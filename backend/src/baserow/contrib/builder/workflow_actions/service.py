from typing import List

from django.contrib.auth.models import AbstractUser

from baserow.contrib.builder.elements.models import Element
from baserow.contrib.builder.workflow_actions.handler import (
    BuilderWorkflowActionHandler,
)
from baserow.contrib.builder.workflow_actions.models import (
    WorkflowAction,
    BuilderWorkflowAction,
)
from baserow.contrib.builder.workflow_actions.operations import (
    CreateBuilderWorkflowActionOperationType,
    DeleteBuilderWorkflowActionOperationType,
    ListBuilderWorkflowActionsElementOperationType,
    ReadBuilderWorkflowActionOperationType,
    UpdateBuilderWorkflowActionOperationType,
)
from baserow.contrib.builder.workflow_actions.signals import (
    workflow_action_created,
    workflow_action_deleted,
    workflow_action_updated,
)
from baserow.contrib.builder.workflow_actions.workflow_action_types import (
    BuilderWorkflowActionType,
)
from baserow.core.handler import CoreHandler


class BuilderWorkflowActionService:
    def __init__(self):
        self.handler = BuilderWorkflowActionHandler()

    def get_workflow_action(
        self, user: AbstractUser, workflow_action_id: int
    ) -> WorkflowAction:
        """
        Returns an workflow_action instance from the database. Also checks the user permissions.

        :param user: The user trying to get the workflow_action
        :param workflow_action_id: The ID of the workflow_action
        :return: The workflow_action instance
        """

        workflow_action = self.handler.get_workflow_action(workflow_action_id)

        CoreHandler().check_permissions(
            user,
            ReadBuilderWorkflowActionOperationType.type,
            workspace=workflow_action.element.page.builder.workspace,
            context=workflow_action,
        )

        return workflow_action

    def get_workflow_actions(
        self,
        user: AbstractUser,
        element: Element,
    ) -> List[WorkflowAction]:
        """
        Gets all the workflow_actions of a given page visible to the given user.

        :param user: The user trying to get the workflow_actions.
        :param element: The element that holds the workflow_actions.
        :return: The workflow_actions of that page.
        """

        CoreHandler().check_permissions(
            user,
            ListBuilderWorkflowActionsElementOperationType.type,
            workspace=element.page.builder.workspace,
            context=element,
        )

        user_workflow_actions = CoreHandler().filter_queryset(
            user,
            ListBuilderWorkflowActionsElementOperationType.type,
            BuilderWorkflowAction.objects.all(),
            workspace=element.page.builder.workspace,
            context=element,
        )

        return self.handler.get_workflow_actions(
            element, base_queryset=user_workflow_actions
        )

    def create_workflow_action(
        self,
        user: AbstractUser,
        workflow_action_type: BuilderWorkflowActionType,
        element: Element,
        **kwargs,
    ) -> WorkflowAction:
        """
        Creates a new workflow_action for a page given the user permissions.

        :param user: The user trying to create the workflow_action.
        :param workflow_action_type: The type of the workflow_action.
        :param element: The element the workflow_action is associated with.
        :param kwargs: Additional attributes of the workflow_action.
        :return: The created workflow_action.
        """

        CoreHandler().check_permissions(
            user,
            CreateBuilderWorkflowActionOperationType.type,
            workspace=element.page.builder.workspace,
            context=element,
        )

        new_workflow_action = self.handler.create_workflow_action(
            workflow_action_type, element=element, **kwargs
        )

        workflow_action_created.send(
            self,
            workflow_action=new_workflow_action,
            user=user,
        )

        return new_workflow_action

    def update_workflow_action(
        self, user: AbstractUser, workflow_action: WorkflowAction, **kwargs
    ) -> WorkflowAction:
        """
        Updates and workflow_action with values. Will also check if the values are allowed
        to be set on the workflow_action first.

        :param user: The user trying to update the workflow_action.
        :param workflow_action: The workflow_action that should be updated.
        :param kwargs: Additional attributes of the workflow_action.
        :return: The updated workflow_action.
        """

        CoreHandler().check_permissions(
            user,
            UpdateBuilderWorkflowActionOperationType.type,
            workspace=workflow_action.element.page.builder.workspace,
            context=workflow_action,
        )

        workflow_action = self.handler.update_workflow_action(workflow_action, **kwargs)

        workflow_action_updated.send(self, workflow_action=workflow_action, user=user)

        return workflow_action

    def delete_workflow_action(
        self, user: AbstractUser, workflow_action: WorkflowAction
    ):
        """
        Deletes a workflow_action.

        :param user: The user trying to delete the workflow_action.
        :param workflow_action: The to-be-deleted workflow_action.
        """

        element = workflow_action.element

        CoreHandler().check_permissions(
            user,
            DeleteBuilderWorkflowActionOperationType.type,
            workspace=element.page.builder.workspace,
            context=workflow_action,
        )

        self.handler.delete_workflow_action(workflow_action)

        workflow_action_deleted.send(
            self, workflow_action_id=workflow_action.id, element=element, user=user
        )
