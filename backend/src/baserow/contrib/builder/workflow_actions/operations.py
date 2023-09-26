from abc import ABC

from baserow.contrib.builder.elements.operations import BuilderElementOperationType
from baserow.core.registries import OperationType


class ListBuilderWorkflowActionsElementOperationType(BuilderElementOperationType):
    type = "builder.element.list_workflow_actions"
    object_scope_name = "builder_workflow_action"


class CreateBuilderWorkflowActionOperationType(BuilderElementOperationType):
    type = "builder.element.create_workflow_action"


class BuilderWorkflowActionOperationType(OperationType, ABC):
    context_scope_name = "builder_workflow_action"


class DeleteBuilderWorkflowActionOperationType(BuilderWorkflowActionOperationType):
    type = "builder.element.workflow_action.delete"


class UpdateBuilderWorkflowActionOperationType(BuilderWorkflowActionOperationType):
    type = "builder.element.workflow_action.update"


class ReadBuilderWorkflowActionOperationType(BuilderWorkflowActionOperationType):
    type = "builder.element.workflow_action.read"
