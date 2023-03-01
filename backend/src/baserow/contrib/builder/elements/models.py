from django.contrib.contenttypes.models import ContentType
from django.db import models

from baserow.contrib.builder.pages.models import Page
from baserow.core.mixins import (
    CreatedAndUpdatedOnMixin,
    HierarchicalModelMixin,
    OrderableMixin,
    PolymorphicContentTypeMixin,
    TrashableModelMixin,
)


def get_default_element_content_type():
    return ContentType.objects.get_for_model(Element)


class Element(
    HierarchicalModelMixin,
    TrashableModelMixin,
    CreatedAndUpdatedOnMixin,
    OrderableMixin,
    PolymorphicContentTypeMixin,
    models.Model,
):
    """ """

    # uid?
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(help_text="Lowest first.")
    content_type = models.ForeignKey(
        ContentType,
        verbose_name="content type",
        related_name="page_elements",
        on_delete=models.SET(get_default_element_content_type),
    )
    # config = models.JSONField(default=dict)
    # style = models.JSONField(default=dict)
    # visibility
    # events->actions

    class Meta:
        ordering = ("order",)

    def get_parent(self):
        return self.page

    @classmethod
    def get_last_order(cls, page):
        queryset = Element.objects.filter(page=page)
        return cls.get_highest_order_of_queryset(queryset) + 1


def default_expression():
    return {"type": "plain", "value": ""}


class ExpressionField(models.JSONField):
    """
    An expression that can reference a data source, a formula or a plain value.
    """

    def __init__(self, *args, **kwargs):
        kwargs["default"] = kwargs.get("default", default_expression)
        super().__init__(*args, **kwargs)


class BaseTextElement(Element):
    value = ExpressionField()

    class Meta:
        abstract = True


class HeadingElement(BaseTextElement):
    class HeadingLevel(models.IntegerChoices):
        H1 = 1
        H2 = 2
        H3 = 3
        H4 = 4
        H5 = 5

    level = models.IntegerField(choices=HeadingLevel.choices, default=1)


class ParagraphElement(BaseTextElement):
    ...
