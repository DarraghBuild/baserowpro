from typing import Any, Dict, Union

from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DRFValidationError

from baserow.contrib.builder.api.workflow_actions.serializers import (
    BuilderWorkflowServiceActionTypeSerializer,
    UpsertRowWorkflowActionTypeSerializer,
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
from baserow.contrib.database.fields.exceptions import FieldDoesNotExist
from baserow.contrib.database.fields.handler import FieldHandler
from baserow.contrib.database.table.exceptions import TableDoesNotExist
from baserow.contrib.database.table.handler import TableHandler
from baserow.contrib.integrations.local_baserow.api.serializers import (
    LocalBaserowTableServiceFieldMappingSerializer,
)
from baserow.contrib.integrations.local_baserow.models import (
    LocalBaserowTableServiceFieldMapping,
)
from baserow.core.formula.serializers import FormulaSerializerField
from baserow.core.formula.types import BaserowFormula
from baserow.core.integrations.exceptions import IntegrationDoesNotExist
from baserow.core.integrations.handler import IntegrationHandler
from baserow.core.services.handler import ServiceHandler
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
    serializer_mixins = [BuilderWorkflowServiceActionTypeSerializer]
    serializer_field_overrides = {
        "service": serializers.SerializerMethodField(help_text="", source="service"),
    }

    class SerializedDict(BuilderWorkflowActionDict):
        service: Dict

    @property
    def allowed_fields(self):
        return super().allowed_fields + ["service_id"]

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
    serializer_mixins = [UpsertRowWorkflowActionTypeSerializer]
    request_serializer_field_overrides = {
        "table_id": serializers.IntegerField(
            required=False,
            allow_null=True,
            help_text="The Baserow table which we should use "
            "when inserting or updating rows.",
        ),
        "integration_id": serializers.IntegerField(
            required=False,
            allow_null=True,
            help_text="The Baserow integration we should use.",
        ),
        "field_mappings": LocalBaserowTableServiceFieldMappingSerializer(
            required=False, many=True, source="service.field_mappings"
        ),
    }
    request_serializer_field_names = ["table_id", "integration_id", "field_mappings"]

    @property
    def serializer_field_names(self):
        return super().serializer_field_names + [
            "table_id",
            "integration_id",
            "field_mappings",
        ]

    @property
    def allowed_fields(self):
        return super().allowed_fields + ["table_id", "integration_id"]

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
        integration = None
        integration_id = values.pop("integration_id", None)
        if integration_id:
            try:
                integration = IntegrationHandler().get_integration(integration_id)
            except IntegrationDoesNotExist:
                raise DRFValidationError(
                    f"The integration with ID {integration_id} does not exist."
                )

        table = None
        table_id = values.pop("table_id", None)
        if table_id:
            try:
                table = TableHandler().get_table(table_id)
            except TableDoesNotExist:
                raise DRFValidationError(
                    f"The table with ID {table_id} does not exist."
                )

        row_id = values.pop("row_id", "")
        if instance is None:
            service = ServiceHandler().create_service(
                service_type_registry.get("local_baserow_upsert_row"),
                table=table,
                row_id=row_id,
                integration=integration,
            )
            values["service_id"] = service.pk
        else:
            service = instance.service.specific

            # Did the table change? If it did, we need to nuke the field
            # mappings that are present. An enhancement in the future would
            # be to check if they relate to the new table, or the old one.
            if service.table_id and service.table_id != table_id:
                values["field_mappings"] = []

            # On a PATCH if no `service_id` value is provided, then `service_id`
            # is given a `None` value by DRF, so here we set it properly.
            values["service_id"] = service.id

            if service.table_id != table_id or service.row_id != row_id:
                service.table = table
                service.row_id = row_id
                service.save()

            if service.integration_id != integration_id:
                service.integration = integration
                service.save()

        if "field_mappings" in values and service.table_id:
            bulk_field_mappings = []
            service.field_mappings.all().delete()
            base_field_qs = service.table.field_set.all()
            for field_mapping in values["field_mappings"]:
                try:
                    field = FieldHandler().get_field(
                        field_mapping["field_id"], base_queryset=base_field_qs
                    )
                except KeyError:
                    raise DRFValidationError("A field mapping must have a `field_id`.")
                except FieldDoesNotExist as exc:
                    raise DRFValidationError(str(exc))

                bulk_field_mappings.append(
                    LocalBaserowTableServiceFieldMapping(
                        field=field, service=service, value=field_mapping["value"]
                    )
                )
            LocalBaserowTableServiceFieldMapping.objects.bulk_create(
                bulk_field_mappings
            )

        return super().prepare_value_for_db(values, instance=instance)


class CreateRowWorkflowActionType(UpsertRowWorkflowActionType):
    type = "create_row"
    model_class = LocalBaserowCreateRowWorkflowAction

    @property
    def allowed_fields(self):
        return super().allowed_fields + ["field_mappings"]


class UpdateRowWorkflowActionType(UpsertRowWorkflowActionType):
    type = "update_row"
    model_class = LocalBaserowUpdateRowWorkflowAction

    @property
    def allowed_fields(self):
        return super().allowed_fields + ["row_id", "field_mappings"]

    @property
    def serializer_field_names(self):
        return super().serializer_field_names + ["row_id"]

    @property
    def request_serializer_field_names(self):
        return super().request_serializer_field_names + ["row_id"]

    @property
    def request_serializer_field_overrides(self):
        return super().request_serializer_field_overrides | {
            "row_id": FormulaSerializerField(
                required=False,
                allow_blank=True,
                help_text="A formula for defining the intended row.",
            )
        }
