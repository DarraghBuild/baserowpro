from django.conf import settings
from django.db import transaction
from django.db.models import QuerySet
from django.utils import timezone

from celery import group
from celery.schedules import crontab

from baserow.config.celery import app
from baserow.contrib.database.fields.registries import field_type_registry
from baserow.core.models import Group


def filter_distinct_group_ids_per_fields(queryset: QuerySet) -> QuerySet:
    """
    Filters the provided queryset to only return the distinct group ids.

    :param queryset: The queryset that should be filtered.
    """

    return Group.objects.filter(application__database__table__field__in=queryset)


@app.task(bind=True, queue=settings.PERIODIC_FIELD_UPDATE_QUEUE_NAME)
def run_periodic_fields_updates(self):
    """
    Refreshes all the fields that need to be updated periodically for all
    groups.
    """

    for field_type_instance in field_type_registry.get_all():
        field_qs = field_type_instance.get_fields_needing_periodic_update()
        if field_qs is None:
            continue

        group_qs = filter_distinct_group_ids_per_fields(field_qs)

        field_type = field_type_instance.type
        update_tasks = [
            run_periodic_field_type_update_per_group.s(field_type, group_id)
            for group_id in group_qs.values_list("id", flat=True)
        ]

        group(update_tasks).apply_async()


@app.task(bind=True, queue=settings.PERIODIC_FIELD_UPDATE_QUEUE_NAME)
def run_periodic_field_type_update_per_group(self, field_type: str, group_id: int):
    """
    Refreshes the formulas that need to be updated periodically for the provided
    group.

    :param field_type: The type of the field that needs to be refreshed.
    :param group_id: The id of the group for which the formulas must be refreshed.
    """

    field_type_instance = field_type_registry.get(field_type)
    qs = field_type_instance.get_fields_needing_periodic_update()
    if qs is None:
        return

    updated_groups = Group.objects.filter(id=group_id).update(now=timezone.now())
    if updated_groups == 0:
        return

    for field in qs.filter(table__database__group_id=group_id):
        with transaction.atomic():
            field_type_instance.run_periodic_update(field)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    update_interval = settings.PERIODIC_FIELD_UPDATE_INTERVAL_MINUTES
    sender.add_periodic_task(
        crontab(minute=f"*/{update_interval}"), run_periodic_fields_updates.s()
    )
