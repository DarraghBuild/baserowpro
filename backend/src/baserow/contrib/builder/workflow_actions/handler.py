from typing import Iterable, Optional

from django.db.models import QuerySet

from baserow.contrib.builder.pages.models import Page
from baserow.contrib.builder.workflow_actions.models import BuilderWorkflowAction
from baserow.contrib.builder.workflow_actions.registries import (
    builder_workflow_action_type_registry,
)
from baserow.core.db import specific_iterator
from baserow.core.workflow_actions.handler import WorkflowActionHandler
from baserow.core.workflow_actions.models import WorkflowAction


class BuilderWorkflowActionHandler(WorkflowActionHandler):
    model = BuilderWorkflowAction
    registry = builder_workflow_action_type_registry

    def get_workflow_actions(
        self, page: Page, base_queryset: Optional[QuerySet] = None
    ) -> Iterable[WorkflowAction]:
        """
        Get all the workflow actions of an page

        :param page: The page associated with the workflow actions
        :param base_queryset: Optional base queryset to filter the results
        :return: A list of workflow actions
        """

        if base_queryset is None:
            base_queryset = self.model.objects

        return specific_iterator(base_queryset.filter(page=page))
