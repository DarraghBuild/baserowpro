from typing import List, Optional

from django.db.models import QuerySet

from baserow.contrib.builder.elements.models import Element
from baserow.contrib.builder.workflow_actions.models import BuilderWorkflowAction
from baserow.core.workflow_actions.handler import WorkflowActionHandler
from baserow.core.workflow_actions.models import WorkflowAction


class BuilderWorkflowActionHandler(WorkflowActionHandler):
    model = BuilderWorkflowAction

    def get_workflow_actions(
        self, element: Element, base_queryset: Optional[QuerySet] = None
    ) -> List[WorkflowAction]:
        """
        Get all the workflow actions of an element

        :param element: The element associated with the workflow actions
        :param base_queryset: Optional base queryset to filter the results
        :return: A list of workflow actions
        """

        if base_queryset is None:
            base_queryset = self.model.objects

        return base_queryset.filter(element=element)
