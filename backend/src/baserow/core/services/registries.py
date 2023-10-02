from abc import ABC
from typing import Any, Dict, Optional, Type, TypeVar

from django.contrib.auth.models import AbstractUser

from baserow.core.formula.runtime_formula_context import RuntimeFormulaContext
from baserow.core.integrations.handler import IntegrationHandler
from baserow.core.integrations.models import Integration
from baserow.core.registry import (
    CustomFieldsInstanceMixin,
    CustomFieldsRegistryMixin,
    ImportExportMixin,
    Instance,
    ModelInstanceMixin,
    ModelRegistryMixin,
    Registry,
)

from .models import Service
from .types import ServiceDictSubClass, ServiceSubClass


class ServiceType(
    ModelInstanceMixin[Service],
    ImportExportMixin[ServiceSubClass],
    CustomFieldsInstanceMixin,
    Instance,
    ABC,
):
    """
    A service type describe a specific service of an external integration.
    """

    SerializedDict: Type[ServiceDictSubClass]

    # The maximum number of records this service is able to return.
    # By default, the maximum is `None`, which is unlimited.
    max_result_limit = None

    # The default number of records this service will return,
    # unless instructed otherwise by a user.
    default_result_limit = max_result_limit

    # Does this service return a list of record?
    returns_list = False

    def prepare_values(
        self, values: Dict[str, Any], user: AbstractUser
    ) -> Dict[str, Any]:
        """
        The prepare_values hook gives the possibility to change the provided values
        that just before they are going to be used to create or update the instance. For
        example if an ID is provided, it can be converted to a model instance. Or to
        convert a certain date string to a date object. It's also an opportunity to add
        specific validations.

        :param values: The provided values.
        :param user: The user on whose behalf the change is made.
        :return: The updated values.
        """

        # We load the actual integration object
        if "integration_id" in values:
            integration_id = values.pop("integration_id")
            if integration_id is not None:
                integration = IntegrationHandler().get_integration(integration_id)
                values["integration"] = integration
            else:
                values["integration"] = None

        return values

    def dispatch_transform(
        self,
        data: Any,
    ) -> Any:
        """
        Responsible for taking the `dispatch_data` result and transforming its value
        for API consumer's consumption.

        :param data: The `dispatch_data` result.
        :return: The transformed `dispatch_transform` result if any.
        """

    def dispatch_data(
        self,
        service: ServiceSubClass,
        runtime_formula_context: RuntimeFormulaContext,
    ) -> Any:
        """
        Responsible for executing the service's principle task.

        :param service: The service instance to dispatch with.
        :param runtime_formula_context: The runtime_formula_context instance used to
            resolve formulas (if any).
        :return: The service `dispatch_data` result if any.
        """

    def dispatch(
        self,
        service: ServiceSubClass,
        runtime_formula_context: RuntimeFormulaContext,
    ) -> Any:
        """
        Responsible for calling `dispatch_data` and `dispatch_transform` to execute
        the service's task, and generating the dispatch's response, respectively.

        :param service: The service instance to dispatch with.
        :param runtime_formula_context: The runtime_formula_context instance used to
            resolve formulas (if any).
        :return: The service dispatch result if any.
        """

        data = self.dispatch_data(service, runtime_formula_context)
        return self.dispatch_transform(data)

    def get_property_for_serialization(self, service: Service, prop_name: str):
        """
        This hooks allow to customize the serialization of a property.
        """

        if prop_name == "type":
            return self.type

        return getattr(service, prop_name)

    def get_schema_name(self, service: Service) -> str:
        """
        The default schema name added to the `title` in a JSON Schema object.

        :param service: The service we want to generate a schema `title` with.
        :return: A string.
        """

        return f"Service{service.id}Schema"

    def generate_schema(self, service: Service) -> Optional[Dict[str, Any]]:
        """
        Responsible for generating the full JSON Schema response. Must be
        overridden by child classes so that the can return their service's
        schema.

        :param service: The service we want to generate a schema for.
        :return: None, or a dictionary representing the schema.
        """

        return None

    def export_serialized(
        self,
        service: Service,
    ) -> ServiceDictSubClass:
        """Serialize the service"""

        property_names = self.SerializedDict.__annotations__.keys()

        serialized = self.SerializedDict(
            **{
                key: self.get_property_for_serialization(service, key)
                for key in property_names
            }
        )

        return serialized

    def transform_serialized_value(
        self, prop_name: str, value: Any, id_mapping: Dict[str, Any]
    ):
        """
        This hooks allow to customize the deserialization of a property.

        :param prop_name: the name of the property being transformed.
        :param value: the value of this property.
        :param id_mapping: the id mapping dict.
        """

        return value

    def import_serialized(
        self,
        integration: Integration,
        serialized_values: Dict[str, Any],
        id_mapping: Dict[str, Any],
    ) -> Service:
        """Import a previously serialized service."""

        if "services" not in id_mapping:
            id_mapping["services"] = {}

        serialized_copy = serialized_values.copy()

        # We remove the integration_id key here because it has already been consumed
        # by the parent
        property_names = [
            p
            for p in self.SerializedDict.__annotations__.keys()
            if p != "integration_id"
        ]

        for name in property_names:
            serialized_copy[name] = self.transform_serialized_value(
                name, serialized_copy[name], id_mapping
            )

        # Remove extra keys
        service_exported_id = serialized_copy.pop("id")
        serialized_copy.pop("type")

        service = self.model_class(integration=integration, **serialized_copy)
        service.save()

        id_mapping["services"][service_exported_id] = service.id

        return service

    def enhance_queryset(self, queryset):
        """
        Allow to enhance the queryset when querying the service mainly to improve
        performances.
        """

        return queryset


ServiceTypeSubClass = TypeVar("ServiceTypeSubClass", bound=ServiceType)


class ServiceTypeRegistry(
    ModelRegistryMixin[ServiceSubClass, ServiceTypeSubClass],
    Registry[ServiceTypeSubClass],
    CustomFieldsRegistryMixin,
):
    """
    Contains the registered service types.
    """

    name = "integration_service"


service_type_registry: ServiceTypeRegistry = ServiceTypeRegistry()
