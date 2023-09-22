from baserow.core.registry import (
    CustomFieldsRegistryMixin,
    ModelRegistryMixin,
    Registry,
)
from baserow.core.workflow_actions.registries import WorkflowActionType


class BuilderWorkflowActionTypeRegistry(
    Registry, ModelRegistryMixin, CustomFieldsRegistryMixin
):
    """
    Contains all the registered workflow action types for the builder module.
    """

    name = "builder_workflow_action_type"


builder_workflow_action_type_registry = BuilderWorkflowActionTypeRegistry()
