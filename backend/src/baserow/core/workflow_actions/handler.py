from typing import cast

from baserow.core.utils import extract_allowed
from baserow.core.workflow_actions.models import WorkflowAction
from baserow.core.workflow_actions.registries import WorkflowActionType


class WorkflowActionHandler:
    def create_workflow_action(
        self, workflow_action_type: WorkflowActionType, **kwargs
    ) -> WorkflowAction:
        """
        Creates a new workflow action of the given type.

        :param workflow_action_type: The type of the new workflow action
        :param kwargs: Any fields that need to be set for that specific type
        :return: The created workflow action
        """
        allowed_values = extract_allowed(kwargs, workflow_action_type.allowed_fields)

        model_class = cast(WorkflowAction, workflow_action_type.model_class)

        workflow_action = model_class(**allowed_values)
        workflow_action.save()

        return workflow_action

    def delete_workflow_action(self, workflow_action: WorkflowAction):
        """
        Deletes a given workflow action.

        :param workflow_action: The workflow action to be deleted
        """

        workflow_action.delete()

    def update_workflow_action(
        self, workflow_action: WorkflowAction, **kwargs
    ) -> WorkflowAction:
        """
        Update an existing workflow action.

        :param workflow_action: The workflow action you want to update.
        :param kwargs: The updates you wish to perform on the workflow action.
        :return: The updated workflow action.
        """

        allowed_updates = extract_allowed(
            kwargs, workflow_action.get_type().allowed_fields
        )

        for key, value in allowed_updates.items():
            setattr(workflow_action, key, value)

        workflow_action.save()

        return workflow_action
