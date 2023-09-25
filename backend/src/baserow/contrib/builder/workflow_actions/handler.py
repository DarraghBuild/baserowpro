from typing import List

from baserow.contrib.builder.elements.models import Element
from baserow.contrib.builder.workflow_actions.models import BuilderWorkflowAction
from baserow.core.workflow_actions.handler import WorkflowActionHandler
from baserow.core.workflow_actions.models import WorkflowAction


class BuilderWorkflowActionHandler(WorkflowActionHandler):
    model = BuilderWorkflowAction

    def get_workflow_actions(self, element: Element) -> List[WorkflowAction]:
        return self.model.objects.filter(element=element)
