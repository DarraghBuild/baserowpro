from abc import ABC
from typing import Any, Dict

from baserow.core.registry import (
    CustomFieldsInstanceMixin,
    ImportExportMixin,
    Instance,
    ModelInstanceMixin,
    T,
)
from baserow.core.workflow_actions.models import WorkflowAction


class WorkflowActionType(
    Instance, ModelInstanceMixin, ImportExportMixin, CustomFieldsInstanceMixin, ABC
):
    def export_serialized(self, instance: T) -> Dict[str, Any]:
        return instance  # TODO

    def import_serialized(
        self, parent: Any, serialized_values: Dict[str, Any], id_mapping: Dict
    ) -> T:
        return serialized_values  # TODO

    def prepare_value_for_db(self, values: Dict, instance: WorkflowAction = None):
        """
        A hook which can be called when before a workflow action is created or updated

        :param values: The values that are about to be set on the workflow action
        :param instance: The current instance (only when an update happens)
        :return: The prepared values
        """

        return values
