from typing import List, TypedDict


class Expression(TypedDict):
    type: str
    expression: str


class ElementDict(TypedDict):
    id: int
    order: int
    type: str


class PageDict(TypedDict):
    id: int
    name: str
    order: int
    elements: List[ElementDict]


class BuilderDict(TypedDict):
    id: int
    name: str
    order: int
    type: str
    pages: List[PageDict]
