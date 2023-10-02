from abc import abstractmethod
from typing import Dict, Any, TYPE_CHECKING

from baserow.contrib.builder.elements.handler import ElementHandler
from baserow.contrib.builder.workflow_actions.models import (
    NotificationWorkflowAction,
    BuilderWorkflowAction,
)
from baserow.contrib.builder.workflow_actions.types import BuilderWorkflowActionDict
from baserow.core.formula.serializers import FormulaSerializerField
from baserow.core.workflow_actions.registries import WorkflowActionType

if TYPE_CHECKING:
    from baserow.contrib.builder.pages.models import Page


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

    def import_serialized(
        self, page: "Page", serialized_values: Dict[str, Any], id_mapping: Dict
    ) -> BuilderWorkflowAction:
        if "builder_workflow_actions" not in id_mapping:
            id_mapping["builder_workflow_actions"] = {}

        serialized_copy = serialized_values.copy()

        # Remove extra keys
        workflow_action_id = serialized_copy.pop("id")
        serialized_copy.pop("type")

        # Convert table id
        serialized_copy["page_id"] = id_mapping["builder_pages"][
            serialized_copy["page_id"]
        ]

        # Convert element id
        if "element_id" in serialized_copy:
            serialized_copy["element_id"] = id_mapping["builder_page_elements"][
                serialized_copy["element_id"]
            ]

        workflow_action = self.model_class(page=page, **serialized_copy)
        workflow_action.save()

        id_mapping["builder_workflow_actions"][workflow_action_id] = workflow_action.id

        return workflow_action


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
