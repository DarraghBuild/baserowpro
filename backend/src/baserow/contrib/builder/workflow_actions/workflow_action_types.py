from baserow.contrib.builder.workflow_actions.models import NotificationWorkflowAction
from baserow.core.workflow_actions.registries import WorkflowActionType


class NotificationWorkflowActionType(WorkflowActionType):
    type = "notification"
    model_class = NotificationWorkflowAction
