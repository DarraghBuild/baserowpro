from baserow.contrib.builder.workflow_actions.models import BuilderWorkflowAction
from baserow.core.workflow_actions.handler import WorkflowActionHandler


class BuilderWorkflowActionHandler(WorkflowActionHandler):
    model = BuilderWorkflowAction
