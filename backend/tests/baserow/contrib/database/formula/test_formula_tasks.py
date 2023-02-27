from datetime import datetime

from django.db import connection
from django.test.utils import CaptureQueriesContext

import pytest
import pytz
from freezegun import freeze_time

from baserow.contrib.database.fields.field_types import FormulaFieldType
from baserow.contrib.database.fields.registries import field_type_registry
from baserow.contrib.database.formula.tasks import (
    run_periodic_field_type_update_per_group,
)


@pytest.mark.django_db
def test_run_periodic_field_type_update_per_non_existing_group_does_nothing():
    with CaptureQueriesContext(connection) as ctx:
        result = run_periodic_field_type_update_per_group.apply(
            [FormulaFieldType.type, 9999]
        )
        assert result.successful()
        assert len(ctx.captured_queries) == 1


@pytest.mark.django_db
def test_run_periodic_field_type_update_per_non_existing_field_type_raise_error():
    with pytest.raises(field_type_registry.does_not_exist_exception_class):
        run_periodic_field_type_update_per_group.apply(
            ["not_existing_field_type", 9999]
        )


@pytest.mark.django_db
def test_run_periodic_field_type_update_per_group(data_fixture):
    with freeze_time("2023-02-27 10:00"):
        group = data_fixture.create_group()

    database = data_fixture.create_database_application(group=group)
    table = data_fixture.create_database_table(database=database)
    field = data_fixture.create_formula_field(
        table=table, formula="now_utc()", date_include_time=True
    )

    table_model = table.get_model()
    row = table_model.objects.create()

    assert getattr(row, f"field_{field.id}") == datetime(
        2023, 2, 27, 10, 0, 0, tzinfo=pytz.UTC
    )

    with freeze_time("2023-02-27 10:30"):
        result = run_periodic_field_type_update_per_group.apply(
            [FormulaFieldType.type, group.id]
        )
        assert result.successful()

        row.refresh_from_db()
        assert getattr(row, f"field_{field.id}") == datetime(
            2023, 2, 27, 10, 30, 0, tzinfo=pytz.UTC
        )


@pytest.mark.django_db
def test_run_field_type_updates_dependant_fields(data_fixture):
    with freeze_time("2023-02-27 10:15"):
        group = data_fixture.create_group()

    database = data_fixture.create_database_application(group=group)
    table = data_fixture.create_database_table(database=database)
    field = data_fixture.create_formula_field(
        table=table, formula="now_utc()", date_include_time=True
    )
    dependant = data_fixture.create_formula_field(
        table=table, formula=f"field('{field.name}')", date_include_time=True
    )
    dependant_2 = data_fixture.create_formula_field(
        table=table, formula=f"field('{field.name}')", date_include_time=True
    )

    table_model = table.get_model()
    row = table_model.objects.create()

    assert getattr(row, f"field_{field.id}") == datetime(
        2023, 2, 27, 10, 15, 0, tzinfo=pytz.UTC
    )
    assert getattr(row, f"field_{dependant.id}") == datetime(
        2023, 2, 27, 10, 15, 0, tzinfo=pytz.UTC
    )
    assert getattr(row, f"field_{dependant_2.id}") == datetime(
        2023, 2, 27, 10, 15, 0, tzinfo=pytz.UTC
    )

    with freeze_time("2023-02-27 10:45"):
        result = run_periodic_field_type_update_per_group.apply(
            [FormulaFieldType.type, group.id]
        )
        assert result.successful()

        row.refresh_from_db()
        assert getattr(row, f"field_{field.id}") == datetime(
            2023, 2, 27, 10, 45, 0, tzinfo=pytz.UTC
        )
        assert getattr(row, f"field_{dependant.id}") == datetime(
            2023, 2, 27, 10, 45, 0, tzinfo=pytz.UTC
        )
        assert getattr(row, f"field_{dependant_2.id}") == datetime(
            2023, 2, 27, 10, 45, 0, tzinfo=pytz.UTC
        )
