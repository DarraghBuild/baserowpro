from abc import abstractmethod
from typing import Dict, Any

from baserow.contrib.builder.elements.handler import ElementHandler
from baserow.contrib.builder.workflow_actions.models import (
    NotificationWorkflowAction,
    BuilderWorkflowAction,
)
from baserow.contrib.builder.workflow_actions.types import BuilderWorkflowActionDict
from baserow.core.formula.serializers import FormulaSerializerField
from baserow.core.workflow_actions.registries import WorkflowActionType


class BuilderWorkflowActionType(WorkflowActionType):
    allowed_fields = ["page", "element", "element_id", "event"]

    def prepare_value_for_db(
        self, values: Dict, instance: BuilderWorkflowAction = None
    ):
        if "element_id" in values:
            values["element"] = ElementHandler().get_element(values["element_id"])

        return super().prepare_value_for_db(values, instance=instance)

    @abstractmethod
    def get_sample_params(self) -> Dict[str, Any]:
        pass


class NotificationWorkflowActionType(BuilderWorkflowActionType):
    type = "notification"
    model_class = NotificationWorkflowAction
    serializer_field_names = ["title", "description"]
    serializer_field_overrides = {
        "title": FormulaSerializerField(
            help_text="The title of the notification. Must be an formula.",
            required=False,
            allow_blank=True,
            default="",
        ),
        "description": FormulaSerializerField(
            help_text="The description of the notification. Must be an formula.",
            required=False,
            allow_blank=True,
            default="",
        ),
    }

    class SerializedDict(BuilderWorkflowActionDict):
        title: str
        description: str

    @property
    def allowed_fields(self):
        return super().allowed_fields + ["title", "description"]

    def get_sample_params(self) -> Dict[str, Any]:
        return {"title": "'hello'", "description": "'there'"}
