from rest_framework import serializers

from baserow.contrib.builder.workflow_actions.models import (
    NotificationWorkflowAction,
    EventTypes,
    BuilderWorkflowAction,
)
from baserow.core.workflow_actions.registries import WorkflowActionType


class BuilderWorkflowActionType(WorkflowActionType):
    allowed_fields = ["page", "element", "element_id", "event"]
    serializer_field_names = ["element_id", "event"]
    serializer_field_overrides = {
        "element_id": serializers.IntegerField(
            help_text="The id of the element this action belongs to", required=False
        ),
        "event": serializers.ChoiceField(
            choices=EventTypes.choices,
            help_text=BuilderWorkflowAction._meta.get_field("event").help_text,
        ),
    }


class NotificationWorkflowActionType(BuilderWorkflowActionType):
    type = "notification"
    model_class = NotificationWorkflowAction
