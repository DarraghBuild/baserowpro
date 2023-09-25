from baserow.contrib.builder.workflow_actions.models import NotificationWorkflowAction
from baserow.core.workflow_actions.registries import WorkflowActionType


class BuilderWorkflowActionType(WorkflowActionType):
    allowed_fields = ["element", "event"]


class NotificationWorkflowActionType(BuilderWorkflowActionType):
    type = "notification"
    model_class = NotificationWorkflowAction
