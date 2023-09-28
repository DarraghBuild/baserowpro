from abc import ABC, abstractmethod
from typing import Type, cast

from baserow.core.registry import Registry
from baserow.core.utils import extract_allowed
from baserow.core.workflow_actions.exceptions import WorkflowActionDoesNotExist
from baserow.core.workflow_actions.models import WorkflowAction
from baserow.core.workflow_actions.registries import WorkflowActionType


class WorkflowActionHandler(ABC):
    """
    This is an abstract handler, each module that wants to use workflow actions will
    need to implement their own handler.
    """

    @property
    @abstractmethod
    def model(self) -> Type[WorkflowAction]:
        pass

    @property
    @abstractmethod
    def registry(self) -> Registry:
        pass

    def get_workflow_action(self, workflow_action_id: int) -> WorkflowAction:
        """
        Returns a workflow action from the database.

        The queryset here is not optional since every module needs to provide their
        own model at least.

        :param workflow_action_id: The ID of the workflow action.
        :return: The workflow action instance.
        """

        try:
            return self.model.objects.get(id=workflow_action_id).specific
        except self.model.DoesNotExist:
            raise WorkflowActionDoesNotExist()

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

        allowed_values = workflow_action_type.prepare_value_for_db(allowed_values)

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

        allowed_updates = workflow_action.get_type().prepare_value_for_db(
            allowed_updates, instance=workflow_action
        )

        if "type" in allowed_updates:
            workflow_action_type = self.registry.get_by_type(allowed_updates["type"])
            self.delete_workflow_action(workflow_action)
            workflow_action = self.create_workflow_action(
                workflow_action_type, **allowed_updates
            )
        else:
            for key, value in allowed_updates.items():
                setattr(workflow_action, key, value)

            workflow_action.save()

        return workflow_action
