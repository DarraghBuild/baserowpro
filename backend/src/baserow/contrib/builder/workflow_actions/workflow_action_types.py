from typing import Any, Dict, Union

from rest_framework import serializers

from baserow.contrib.builder.api.workflow_actions.serializers import (
    PolymorphicServiceRequestSerializer,
    PolymorphicServiceSerializer,
)
from baserow.contrib.builder.formula_importer import import_formula
from baserow.contrib.builder.workflow_actions.models import (
    BuilderWorkflowServiceAction,
    LocalBaserowCreateRowWorkflowAction,
    LocalBaserowUpdateRowWorkflowAction,
    NotificationWorkflowAction,
    OpenPageWorkflowAction,
)
from baserow.contrib.builder.workflow_actions.registries import (
    BuilderWorkflowActionType,
)
from baserow.contrib.builder.workflow_actions.types import BuilderWorkflowActionDict
from baserow.core.formula.serializers import FormulaSerializerField
from baserow.core.formula.types import BaserowFormula
from baserow.core.integrations.handler import IntegrationHandler
from baserow.core.services.registries import service_type_registry


class NotificationWorkflowActionType(BuilderWorkflowActionType):
    type = "notification"
    model_class = NotificationWorkflowAction
    serializer_field_names = ["title", "description"]
    serializer_field_overrides = {
        "title": FormulaSerializerField(
            help_text="The title of the notification. Must be an formula.",
            required=False,
            allow_blank=True,
            default="",
        ),
        "description": FormulaSerializerField(
            help_text="The description of the notification. Must be an formula.",
            required=False,
            allow_blank=True,
            default="",
        ),
    }

    class SerializedDict(BuilderWorkflowActionDict):
        title: BaserowFormula
        description: BaserowFormula

    @property
    def allowed_fields(self):
        return super().allowed_fields + ["title", "description"]

    def get_pytest_params(self, pytest_data_fixture) -> Dict[str, Any]:
        return {"title": "'hello'", "description": "'there'"}

    def deserialize_property(self, prop_name, value, id_mapping: Dict) -> Any:
        """
        Migrate the formulas.
        """

        if prop_name == "title":
            return import_formula(value, id_mapping)

        if prop_name == "description":
            return import_formula(value, id_mapping)

        return super().deserialize_property(prop_name, value, id_mapping)


class OpenPageWorkflowActionType(BuilderWorkflowActionType):
    type = "open_page"
    model_class = OpenPageWorkflowAction
    serializer_field_names = ["url"]
    serializer_field_overrides = {
        "url": FormulaSerializerField(
            help_text="The url to open. Must be an formula.",
            required=False,
            allow_blank=True,
            default="",
        ),
    }

    class SerializedDict(BuilderWorkflowActionDict):
        url: BaserowFormula

    @property
    def allowed_fields(self):
        return super().allowed_fields + ["url"]

    def get_pytest_params(self, pytest_data_fixture) -> Dict[str, Any]:
        return {"url": "'hello'"}

    def deserialize_property(self, prop_name, value, id_mapping: Dict) -> Any:
        """
        Migrate the formulas.
        """

        if prop_name == "url":
            return import_formula(value, id_mapping)

        if prop_name == "description":
            return import_formula(value, id_mapping)

        return super().deserialize_property(prop_name, value, id_mapping)


class BuilderWorkflowServiceActionType(BuilderWorkflowActionType):
    serializer_field_names = ["service"]
    serializer_field_overrides = {
        "service": serializers.SerializerMethodField(
            help_text="The Service this workflow action is dispatched by.",
            source="service",
        ),
    }

    class SerializedDict(BuilderWorkflowActionDict):
        service: Dict

    @property
    def allowed_fields(self):
        return super().allowed_fields + ["service"]

    def get_pytest_params(self, pytest_data_fixture) -> Dict[str, int]:
        service = pytest_data_fixture.create_local_baserow_upsert_row_service()
        return {"service": service}

    def get_pytest_params_serialized(
        self, pytest_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        service_type = service_type_registry.get_by_model(pytest_params["service"])
        return {"service": service_type.export_serialized(pytest_params["service"])}


class UpsertRowWorkflowActionType(BuilderWorkflowServiceActionType):
    type = "upsert_row"
    request_serializer_field_overrides = {
        "service": PolymorphicServiceRequestSerializer(
            default=None,
            required=False,
            help_text="The service which this workflow action is associated with.",
        )
    }
    serializer_field_overrides = {
        "service": PolymorphicServiceSerializer(
            help_text="The service which this workflow action is associated with."
        )
    }
    request_serializer_field_names = ["service"]

    @property
    def allowed_fields(self):
        return super().allowed_fields + ["service"]

    def serialize_property(
        self, workflow_action: BuilderWorkflowServiceAction, prop_name: str
    ):
        """
        You can customize the behavior of the serialization of a property with this
        hook.
        """

        if prop_name == "service":
            specific_service = workflow_action.service.specific
            service_type = service_type_registry.get_by_model(specific_service)
            return service_type.export_serialized(specific_service)
        return super().serialize_property(workflow_action, prop_name)

    def deserialize_property(
        self, prop_name: str, value: Any, id_mapping: Dict[str, Any]
    ) -> Any:
        """
        This hooks allow to customize the deserialization of a property.

        :param prop_name: the name of the property being transformed.
        :param value: the value of this property.
        :param id_mapping: the id mapping dict.
        :return: the deserialized version for this property.
        """

        if prop_name == "service":
            service_type = service_type_registry.get(value["type"])
            parent = IntegrationHandler().get_integration(value["integration_id"])
            return service_type.import_serialized(
                parent, value, id_mapping, import_formula=import_formula
            )
        return super().deserialize_property(prop_name, value, id_mapping)

    def prepare_value_for_db(
        self,
        values: Dict,
        instance: Union[
            LocalBaserowCreateRowWorkflowAction, LocalBaserowUpdateRowWorkflowAction
        ] = None,
    ):
        """
        Responsible for preparing the upsert row workflow action. By default, the
        only step is to pass any `service` data into the upsert row service.

        :param values: The full workflow action values to prepare.
        :param instance: A create or update row workflow action instance.
        :return: The modified workflow action values, prepared.
        """

        service_values = values.pop("service") or {}  # todo: why is service=None
        service = instance.service.specific if instance else None
        service_type = service_type_registry.get("local_baserow_upsert_row")
        prepared_service_values = service_type.prepare_value_for_db(
            service_values, service
        )
        values.update(prepared_service_values)
        return super().prepare_value_for_db(values, instance=instance)


class CreateRowWorkflowActionType(UpsertRowWorkflowActionType):
    type = "create_row"
    model_class = LocalBaserowCreateRowWorkflowAction


class UpdateRowWorkflowActionType(UpsertRowWorkflowActionType):
    type = "update_row"
    model_class = LocalBaserowUpdateRowWorkflowAction
