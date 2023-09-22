from django.db import models

from baserow.core.mixins import (
    CreatedAndUpdatedOnMixin,
    OrderableMixin,
    PolymorphicContentTypeMixin,
)


class WorkflowAction(
    PolymorphicContentTypeMixin,
    CreatedAndUpdatedOnMixin,
    OrderableMixin,
    models.Model,
):
    class Meta:
        abstract = True
