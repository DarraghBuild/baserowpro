from typing import NewType, TypeVar, TypedDict, List

from baserow.contrib.builder.types import ElementDict

from .models import Element
from ..workflow_actions.models import BuilderWorkflowAction

ElementDictSubClass = TypeVar("ElementDictSubClass", bound=ElementDict)
ElementSubClass = TypeVar("ElementSubClass", bound=Element)

ElementForUpdate = NewType("ElementForUpdate", Element)


class ElementsAndWorkflowActions(TypedDict):
    elements: List[Element]
    workflow_actions: List[BuilderWorkflowAction]
