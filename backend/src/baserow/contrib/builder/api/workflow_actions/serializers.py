from django.utils.functional import lazy

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from baserow.api.services.serializers import ServiceSerializer
from baserow.api.workflow_actions.serializers import WorkflowActionSerializer
from baserow.contrib.builder.workflow_actions.models import BuilderWorkflowAction
from baserow.contrib.builder.workflow_actions.registries import (
    builder_workflow_action_type_registry,
)
from baserow.contrib.integrations.local_baserow.api.serializers import (
    LocalBaserowTableServiceFieldMappingSerializer,
)


class BuilderWorkflowActionSerializer(WorkflowActionSerializer):
    """
    Basic builder workflow action serializer
    """

    @extend_schema_field(OpenApiTypes.STR)
    def get_type(self, instance):
        return builder_workflow_action_type_registry.get_by_model(
            instance.specific_class
        ).type

    class Meta:
        model = BuilderWorkflowAction
        fields = ("id", "order", "element_id", "type", "event")

        extra_kwargs = {
            "id": {"read_only": True},
            "element_id": {"read_only": True},
        }


class CreateBuilderWorkflowActionSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(
        choices=lazy(builder_workflow_action_type_registry.get_types, list)(),
        required=True,
        help_text="The type of the workflow action",
    )
    element_id = serializers.IntegerField(
        allow_null=True,
        required=False,
        help_text="The id of the element the workflow action is associated with",
    )

    class Meta:
        model = BuilderWorkflowAction
        fields = ("id", "element_id", "type", "event")


class UpdateBuilderWorkflowActionsSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(
        choices=lazy(builder_workflow_action_type_registry.get_types, list)(),
        required=False,
        help_text="The type of the workflow action",
    )

    class Meta:
        model = BuilderWorkflowAction
        fields = ("type",)


class OrderWorkflowActionsSerializer(serializers.Serializer):
    workflow_action_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="The ids of the workflow actions in the order they are supposed to be "
        "set in",
    )
    element_id = serializers.IntegerField(
        required=False, help_text="The element the workflow actions belong to"
    )


class BuilderWorkflowServiceActionTypeSerializer(serializers.Serializer):
    service = serializers.SerializerMethodField()

    def get_service(self, workflow_action):
        from baserow.core.services.registries import service_type_registry

        return service_type_registry.get_serializer(
            workflow_action.service, ServiceSerializer
        ).data


class UpsertRowWorkflowActionTypeSerializer(BuilderWorkflowServiceActionTypeSerializer):
    row_id = serializers.SerializerMethodField(
        help_text="The Baserow row ID which we should use when updating rows.",
    )
    table_id = serializers.SerializerMethodField(
        help_text="The Baserow table which we should use "
        "when inserting or updating rows.",
    )
    integration_id = serializers.SerializerMethodField(
        help_text="The Baserow integration we should use.",
    )
    field_mappings = LocalBaserowTableServiceFieldMappingSerializer(
        required=False, many=True, source="service.field_mappings"
    )

    def get_row_id(self, workflow_action):
        return workflow_action.service.specific.row_id

    def get_integration_id(self, workflow_action):
        return workflow_action.service.specific.integration_id

    def get_table_id(self, workflow_action):
        return workflow_action.service.specific.table_id
