from abc import ABC
from typing import Any, Dict

from baserow.core.registry import (
    CustomFieldsInstanceMixin,
    ImportExportMixin,
    Instance,
    ModelInstanceMixin,
    T,
)


class WorkflowActionType(
    Instance, ModelInstanceMixin, ImportExportMixin, CustomFieldsInstanceMixin, ABC
):
    def export_serialized(self, instance: T) -> Dict[str, Any]:
        return instance  # TODO

    def import_serialized(
        self, parent: Any, serialized_values: Dict[str, Any], id_mapping: Dict
    ) -> T:
        return serialized_values  # TODO
