from abc import ABC, abstractmethod
from typing import Any, Dict, Type

from baserow.core.registry import (
    CustomFieldsInstanceMixin,
    ImportExportMixin,
    Instance,
    ModelInstanceMixin,
)
from baserow.core.workflow_actions.models import WorkflowAction
from baserow.core.workflow_actions.types import WorkflowActionDictSubClass


class WorkflowActionType(
    Instance, ModelInstanceMixin, ImportExportMixin, CustomFieldsInstanceMixin, ABC
):
    SerializedDict: Type[WorkflowActionDictSubClass]

    def export_serialized(self, instance: WorkflowAction) -> Dict[str, Any]:
        property_names = self.SerializedDict.__annotations__.keys()

        serialized = self.SerializedDict(
            **{
                key: self.get_property_for_serialization(instance, key)
                for key in property_names
            }
        )

        return serialized

    def get_property_for_serialization(
        self, workflow_action: WorkflowAction, prop_name: str
    ):
        """
        You can customize the behavior of the serialization of a property with this
        hook.
        """

        if prop_name == "type":
            return self.type

        return getattr(workflow_action, prop_name)

    @abstractmethod
    def import_serialized(
        self, parent: Any, serialized_values: Dict[str, Any], id_mapping: Dict
    ) -> WorkflowAction:
        pass

    def prepare_value_for_db(self, values: Dict, instance: WorkflowAction = None):
        """
        A hook which can be called when before a workflow action is created or updated

        :param values: The values that are about to be set on the workflow action
        :param instance: The current instance (only when an update happens)
        :return: The prepared values
        """

        return values

    @abstractmethod
    def get_sample_params(self) -> Dict[str, Any]:
        """
        Returns a sample of params for this type. This can be used to tests the element
        for instance.
        """
