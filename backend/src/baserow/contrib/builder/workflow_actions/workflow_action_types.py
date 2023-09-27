from baserow.contrib.builder.workflow_actions.models import (
    NotificationWorkflowAction,
)
from baserow.core.formula.serializers import FormulaSerializerField
from baserow.core.workflow_actions.registries import WorkflowActionType


class BuilderWorkflowActionType(WorkflowActionType):
    allowed_fields = ["page", "element", "element_id", "event"]


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

    @property
    def allowed_fields(self):
        return super().allowed_fields + ["title", "description"]
