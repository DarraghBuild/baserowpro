from django.db import models

from baserow.contrib.builder.elements.models import Element
from baserow.contrib.builder.workflow_actions.registries import (
    builder_workflow_action_type_registry,
)
from baserow.core.formula.field import FormulaField
from baserow.core.mixins import WithRegistry
from baserow.core.registry import ModelRegistryMixin
from baserow.core.workflow_actions.models import WorkflowAction


class EventTypes(models.TextChoices):
    CLICK = "click"


class BuilderWorkflowAction(WorkflowAction, WithRegistry):
    event = models.CharField(
        max_length=30,
        choices=EventTypes.choices,
        help_text="The event that triggers the execution",
    )
    element = models.ForeignKey(Element, on_delete=models.CASCADE)

    @staticmethod
    def get_type_registry() -> ModelRegistryMixin:
        return builder_workflow_action_type_registry


class NotificationWorkflowAction(BuilderWorkflowAction):
    title = FormulaField(default="")
    description = FormulaField(default="")
