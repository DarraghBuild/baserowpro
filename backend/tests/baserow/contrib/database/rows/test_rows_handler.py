from datetime import datetime
from decimal import Decimal
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.db import models

import pytest
from freezegun import freeze_time
from pyinstrument import Profiler
from pytz import UTC

from baserow.contrib.database.api.utils import (
    extract_field_ids_from_string,
    get_include_exclude_fields,
)
from baserow.contrib.database.rows.exceptions import RowDoesNotExist
from baserow.contrib.database.rows.handler import RowHandler
from baserow.core.exceptions import UserNotInWorkspace
from baserow.core.trash.handler import TrashHandler


def test_get_field_ids_from_dict():
    handler = RowHandler()
    fields_dict = {
        1: "Included",
        "field_2": "Included",
        "3": "Included",
        "abc": "Not included",
        "fieldd_3": "Not included",
    }
    assert handler.extract_field_ids_from_dict(fields_dict) == [1, 2, 3]


def test_extract_field_ids_from_string():
    assert extract_field_ids_from_string(None) == []
    assert extract_field_ids_from_string("not,something") == []
    assert extract_field_ids_from_string("field_1,field_2") == [1, 2]
    assert extract_field_ids_from_string("field_22,test_8,999") == [22, 8, 999]
    assert extract_field_ids_from_string("is,1,one") == [1]


@pytest.mark.django_db
def test_get_include_exclude_fields(data_fixture):
    table = data_fixture.create_database_table()
    table_2 = data_fixture.create_database_table()
    field_1 = data_fixture.create_text_field(table=table, order=1)
    field_2 = data_fixture.create_text_field(table=table, order=2)
    field_3 = data_fixture.create_text_field(table=table_2, order=3)

    assert get_include_exclude_fields(table, include=None, exclude=None) is None

    assert get_include_exclude_fields(table, include="", exclude="") is None

    fields = get_include_exclude_fields(table, f"field_{field_1.id}")
    assert len(fields) == 1
    assert fields[0].id == field_1.id

    fields = get_include_exclude_fields(
        table, f"field_{field_1.id},field_9999,field_{field_2.id}"
    )
    assert len(fields) == 2
    assert fields[0].id == field_1.id
    assert fields[1].id == field_2.id

    fields = get_include_exclude_fields(table, None, f"field_{field_1.id},field_9999")
    assert len(fields) == 1
    assert fields[0].id == field_2.id

    fields = get_include_exclude_fields(
        table, f"field_{field_1.id},field_{field_2.id}", f"field_{field_1.id}"
    )
    assert len(fields) == 1
    assert fields[0].id == field_2.id

    fields = get_include_exclude_fields(table, f"field_{field_3.id}")
    assert len(fields) == 0

    fields = get_include_exclude_fields(table, None, f"field_{field_3.id}")
    assert len(fields) == 2


@pytest.mark.django_db
def test_extract_manytomany_values(data_fixture):
    row_handler = RowHandler()

    class TemporaryModel1(models.Model):
        class Meta:
            app_label = "test"

    class TemporaryModel2(models.Model):
        field_1 = models.CharField()
        field_2 = models.ManyToManyField(TemporaryModel1)

        class Meta:
            app_label = "test"

    values = {"field_1": "Value 1", "field_2": ["Value 2"]}

    values, manytomany_values = row_handler.extract_manytomany_values(
        values, TemporaryModel2
    )

    assert len(values.keys()) == 1
    assert "field_1" in values
    assert len(manytomany_values.keys()) == 1
    assert "field_2" in manytomany_values


@pytest.mark.django_db
@patch("baserow.contrib.database.rows.signals.rows_created.send")
def test_create_row(send_mock, data_fixture):
    user = data_fixture.create_user()
    user_2 = data_fixture.create_user()
    table = data_fixture.create_database_table(name="Car", user=user)
    name_field = data_fixture.create_text_field(
        table=table, name="Name", text_default="Test"
    )
    speed_field = data_fixture.create_number_field(
        table=table, name="Max speed", number_negative=True
    )
    price_field = data_fixture.create_number_field(
        table=table,
        name="Price",
        number_decimal_places=2,
        number_negative=False,
    )

    handler = RowHandler()

    with pytest.raises(UserNotInWorkspace):
        handler.create_row(user=user_2, table=table)

    row_1 = handler.create_row(
        user=user,
        table=table,
        values={
            name_field.id: "Tesla",
            speed_field.id: 240,
            f"field_{price_field.id}": 59999.99,
            9999: "Must not be added",
        },
    )
    assert getattr(row_1, f"field_{name_field.id}") == "Tesla"
    assert getattr(row_1, f"field_{speed_field.id}") == 240
    assert getattr(row_1, f"field_{price_field.id}") == 59999.99
    assert not getattr(row_1, f"field_9999", None)
    assert row_1.order == 1
    row_1.refresh_from_db()
    assert getattr(row_1, f"field_{name_field.id}") == "Tesla"
    assert getattr(row_1, f"field_{speed_field.id}") == 240
    assert getattr(row_1, f"field_{price_field.id}") == Decimal("59999.99")
    assert not getattr(row_1, f"field_9999", None)
    assert row_1.order == Decimal("1.00000000000000000000")
    assert row_1.needs_background_update

    send_mock.assert_called_once()
    assert send_mock.call_args[1]["rows"][0].id == row_1.id
    assert send_mock.call_args[1]["user"].id == user.id
    assert send_mock.call_args[1]["table"].id == table.id
    assert send_mock.call_args[1]["before"] is None
    assert send_mock.call_args[1]["model"]._generated_table_model

    row_2 = handler.create_row(user=user, table=table)
    assert getattr(row_2, f"field_{name_field.id}") == "Test"
    assert not getattr(row_2, f"field_{speed_field.id}")
    assert not getattr(row_2, f"field_{price_field.id}")
    row_1.refresh_from_db()
    assert row_1.order == Decimal("1.00000000000000000000")
    assert row_2.order == Decimal("2.00000000000000000000")

    row_3 = handler.create_row(user=user, table=table, before_row=row_2)
    row_1.refresh_from_db()
    row_2.refresh_from_db()
    assert row_1.order == Decimal("1.00000000000000000000")
    assert row_2.order == Decimal("2.00000000000000000000")
    assert row_3.order == Decimal("1.50000000000000000000")
    assert send_mock.call_args[1]["before"].id == row_2.id

    row_4 = handler.create_row(user=user, table=table, before_row=row_2)
    row_1.refresh_from_db()
    row_2.refresh_from_db()
    row_3.refresh_from_db()
    assert row_1.order == Decimal("1.00000000000000000000")
    assert row_2.order == Decimal("2.00000000000000000000")
    assert row_3.order == Decimal("1.50000000000000000000")
    assert row_4.order == Decimal("1.66666666666666674068")

    row_5 = handler.create_row(user=user, table=table, before_row=row_3)
    row_1.refresh_from_db()
    row_2.refresh_from_db()
    row_3.refresh_from_db()
    row_4.refresh_from_db()
    assert row_1.order == Decimal("1.00000000000000000000")
    assert row_2.order == Decimal("2.00000000000000000000")
    assert row_3.order == Decimal("1.50000000000000000000")
    assert row_4.order == Decimal("1.66666666666666674068")
    assert row_5.order == Decimal("1.33333333333333325932")

    row_6 = handler.create_row(user=user, table=table, before_row=row_2)
    row_1.refresh_from_db()
    row_2.refresh_from_db()
    row_3.refresh_from_db()
    row_4.refresh_from_db()
    row_5.refresh_from_db()
    assert row_1.order == Decimal("1.00000000000000000000")
    assert row_2.order == Decimal("2.00000000000000000000")
    assert row_3.order == Decimal("1.50000000000000000000")
    assert row_4.order == Decimal("1.66666666666666674068")
    assert row_5.order == Decimal("1.33333333333333325932")
    assert row_6.order == Decimal("1.75000000000000000000")

    row_7 = handler.create_row(user, table=table, before_row=row_1)
    row_1.refresh_from_db()
    row_2.refresh_from_db()
    row_3.refresh_from_db()
    row_4.refresh_from_db()
    row_5.refresh_from_db()
    row_6.refresh_from_db()
    assert row_1.order == Decimal("1.00000000000000000000")
    assert row_2.order == Decimal("2.00000000000000000000")
    assert row_3.order == Decimal("1.50000000000000000000")
    assert row_4.order == Decimal("1.66666666666666674068")
    assert row_5.order == Decimal("1.33333333333333325932")
    assert row_6.order == Decimal("1.75000000000000000000")
    assert row_7.order == Decimal("0.50000000000000000000")

    with pytest.raises(ValidationError):
        handler.create_row(user=user, table=table, values={price_field.id: -10.22})

    model = table.get_model()

    rows = model.objects.all()
    assert len(rows) == 7
    rows_0, rows_1, rows_2, rows_3, rows_4, rows_5, rows_6 = rows
    assert rows_0.id == row_7.id
    assert rows_1.id == row_1.id
    assert rows_2.id == row_5.id
    assert rows_3.id == row_3.id
    assert rows_4.id == row_4.id
    assert rows_5.id == row_6.id
    assert rows_6.id == row_2.id

    row_2.delete()
    row_8 = handler.create_row(user, table=table)
    assert row_8.order == Decimal("3.00000000000000000000")


@pytest.mark.django_db
def test_get_row(data_fixture):
    user = data_fixture.create_user()
    user_2 = data_fixture.create_user()
    table = data_fixture.create_database_table(name="Car", user=user)
    name_field = data_fixture.create_text_field(
        table=table, name="Name", text_default="Test"
    )
    speed_field = data_fixture.create_number_field(
        table=table, name="Max speed", number_negative=True
    )
    price_field = data_fixture.create_number_field(
        table=table,
        name="Price",
        number_decimal_places=2,
        number_negative=False,
    )

    handler = RowHandler()
    row = handler.create_row(
        user=user,
        table=table,
        values={
            f"field_{name_field.id}": "Tesla",
            f"field_{speed_field.id}": 240,
            f"field_{price_field.id}": Decimal("59999.99"),
        },
    )

    with pytest.raises(UserNotInWorkspace):
        handler.get_row(user=user_2, table=table, row_id=row.id)

    with pytest.raises(RowDoesNotExist):
        handler.get_row(user=user, table=table, row_id=99999)

    row_tmp = handler.get_row(user=user, table=table, row_id=row.id)

    assert row_tmp.id == row.id
    assert getattr(row_tmp, f"field_{name_field.id}") == "Tesla"
    assert getattr(row_tmp, f"field_{speed_field.id}") == 240
    assert getattr(row_tmp, f"field_{price_field.id}") == Decimal("59999.99")


@pytest.mark.django_db
def test_get_adjacent_row(data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(name="Car", user=user)
    name_field = data_fixture.create_text_field(
        table=table, name="Name", text_default="Test"
    )

    handler = RowHandler()
    rows = handler.create_rows(
        user=user,
        table=table,
        rows_values=[
            {
                f"field_{name_field.id}": "Tesla",
            },
            {
                f"field_{name_field.id}": "Audi",
            },
            {
                f"field_{name_field.id}": "BMW",
            },
        ],
    )

    queryset = table.get_model().objects.all()
    next_row = handler.get_adjacent_row(rows[1], queryset)
    previous_row = handler.get_adjacent_row(rows[1], queryset, previous=True)

    assert next_row.id == rows[2].id
    assert previous_row.id == rows[0].id


@pytest.mark.django_db
def test_get_adjacent_row_with_custom_filters(data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(name="Car", user=user)
    name_field = data_fixture.create_text_field(
        table=table, name="Name", text_default="Test"
    )

    handler = RowHandler()
    [row_1, row_2, row_3] = handler.create_rows(
        user=user,
        table=table,
        rows_values=[
            {
                f"field_{name_field.id}": "Tesla",
            },
            {
                f"field_{name_field.id}": "Audi",
            },
            {
                f"field_{name_field.id}": "BMW",
            },
        ],
    )

    base_queryset = table.get_model().objects.filter(id__in=[row_2.id, row_3.id])

    next_row = handler.get_adjacent_row(row_2, base_queryset)
    previous_row = handler.get_adjacent_row(row_2, base_queryset, previous=True)

    assert next_row.id == row_3.id
    assert previous_row is None


@pytest.mark.django_db
def test_get_adjacent_row_with_view_sort(data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(name="Car", user=user)
    view = data_fixture.create_grid_view(table=table)
    name_field = data_fixture.create_text_field(
        table=table, name="Name", text_default="Test"
    )

    data_fixture.create_view_sort(view=view, field=name_field, order="DESC")

    handler = RowHandler()
    [row_1, row_2, row_3] = handler.create_rows(
        user=user,
        table=table,
        rows_values=[
            {
                f"field_{name_field.id}": "A",
            },
            {
                f"field_{name_field.id}": "B",
            },
            {
                f"field_{name_field.id}": "C",
            },
        ],
    )

    base_queryset = table.get_model().objects.all()

    next_row = handler.get_adjacent_row(row_2, base_queryset, view=view)
    previous_row = handler.get_adjacent_row(
        row_2, base_queryset, previous=True, view=view
    )

    assert next_row.id == row_1.id
    assert previous_row.id == row_3.id


@pytest.mark.django_db
@pytest.mark.disabled_in_ci
# You must add --run-disabled-in-ci -s to pytest to run this test, you can do this in
# intellij by editing the run config for this test and adding --run-disabled-in-ci -s
# to additional args.
def test_get_adjacent_row_performance_many_rows(data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(name="Car", user=user)
    name_field = data_fixture.create_text_field(
        table=table, name="Name", text_default="Test"
    )

    handler = RowHandler()

    row_amount = 100000
    row_values = [{f"field_{name_field.id}": "Tesla"} for _ in range(row_amount)]

    rows = handler.create_rows(user=user, table=table, rows_values=row_values)

    profiler = Profiler()
    profiler.start()
    next_row = handler.get_adjacent_row(rows[5])
    profiler.stop()

    print(profiler.output_text(unicode=True, color=True))

    assert next_row.id == rows[6].id
    assert table.get_model().objects.count() == row_amount


@pytest.mark.django_db
@pytest.mark.disabled_in_ci
# You must add --run-disabled-in-ci -s to pytest to run this test, you can do this in
# intellij by editing the run config for this test and adding --run-disabled-in-ci -s
# to additional args.
def test_get_adjacent_row_performance_many_fields(data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(name="Car", user=user)

    handler = RowHandler()

    field_amount = 1000
    fields = [
        data_fixture.create_text_field(table=table, name=f"Field_{i}")
        for i in range(field_amount)
    ]

    row_amount = 4000
    row_values = []
    for i in range(row_amount):
        row_value = {f"field_{field.id}": "Tesla" for field in fields}
        row_values.append(row_value)

    rows = handler.create_rows(user=user, table=table, rows_values=row_values)

    profiler = Profiler()
    profiler.start()
    next_row = handler.get_adjacent_row(rows[5])
    profiler.stop()

    print(profiler.output_text(unicode=True, color=True))

    assert next_row.id == rows[6].id
    assert table.get_model().objects.count() == row_amount


@pytest.mark.django_db
@patch("baserow.contrib.database.rows.signals.rows_updated.send")
def test_update_row(send_mock, data_fixture):
    user = data_fixture.create_user()
    user_2 = data_fixture.create_user()
    table = data_fixture.create_database_table(name="Car", user=user)
    name_field = data_fixture.create_text_field(
        table=table, name="Name", text_default="Test"
    )
    speed_field = data_fixture.create_number_field(
        table=table, name="Max speed", number_negative=True
    )
    price_field = data_fixture.create_number_field(
        table=table,
        name="Price",
        number_decimal_places=2,
        number_negative=False,
    )

    handler = RowHandler()
    row = handler.create_row(user=user, table=table)

    with pytest.raises(UserNotInWorkspace):
        handler.update_row_by_id(user=user_2, table=table, row_id=row.id, values={})

    with pytest.raises(RowDoesNotExist):
        handler.update_row_by_id(user=user, table=table, row_id=99999, values={})

    with pytest.raises(ValidationError):
        handler.update_row_by_id(
            user=user, table=table, row_id=row.id, values={price_field.id: -10.99}
        )

    row.needs_background_update = False
    row.save(update_fields=("needs_background_update",))
    with patch(
        "baserow.contrib.database.rows.signals.before_rows_update.send"
    ) as before_send_mock:
        handler.update_row_by_id(
            user=user,
            table=table,
            row_id=row.id,
            values={
                name_field.id: "Tesla",
                speed_field.id: 240,
                f"field_{price_field.id}": 59999.99,
            },
        )
    row.refresh_from_db()

    assert getattr(row, f"field_{name_field.id}") == "Tesla"
    assert getattr(row, f"field_{speed_field.id}") == 240
    assert getattr(row, f"field_{price_field.id}") == Decimal("59999.99")
    assert row.needs_background_update

    before_send_mock.assert_called_once()
    assert before_send_mock.call_args[1]["rows"][0].id == row.id
    assert before_send_mock.call_args[1]["user"].id == user.id
    assert before_send_mock.call_args[1]["table"].id == table.id
    assert before_send_mock.call_args[1]["model"]._generated_table_model

    send_mock.assert_called_once()
    assert send_mock.call_args[1]["rows"][0].id == row.id
    assert send_mock.call_args[1]["user"].id == user.id
    assert send_mock.call_args[1]["table"].id == table.id
    assert send_mock.call_args[1]["model"]._generated_table_model
    assert send_mock.call_args[1]["before_return"] == before_send_mock.return_value


@pytest.mark.django_db
def test_create_rows_created_on_and_last_modified(data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user)
    handler = RowHandler()

    with freeze_time("2020-01-01 12:00"):
        rows = handler.create_rows(user=user, table=table, rows_values=[{}])
        row = rows[0]
        assert row.created_on == datetime(2020, 1, 1, 12, 0, tzinfo=UTC)
        assert row.updated_on == datetime(2020, 1, 1, 12, 0, tzinfo=UTC)


@pytest.mark.django_db
def test_update_rows_created_on_and_last_modified(data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user)
    field = data_fixture.create_text_field(table=table)
    handler = RowHandler()

    with freeze_time("2020-01-01 12:00"):
        row = table.get_model().objects.create()

    with freeze_time("2020-01-02 12:00"):
        rows = handler.update_rows(
            user=user,
            table=table,
            rows=[{"id": row.id, f"field_" f"{field.id}": "Test"}],
        )
        row = rows[0]
        assert row.created_on == datetime(2020, 1, 1, 12, 0, tzinfo=UTC)
        assert row.updated_on == datetime(2020, 1, 2, 12, 0, tzinfo=UTC)


@pytest.mark.django_db
@patch("baserow.contrib.database.rows.signals.rows_created.send")
def test_import_rows(send_mock, data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user)
    name_field = data_fixture.create_text_field(
        table=table, name="Name", text_default="Test", order=1
    )
    speed_field = data_fixture.create_number_field(
        table=table, name="Max speed", number_negative=True, order=2
    )
    price_field = data_fixture.create_number_field(
        table=table,
        name="Price",
        number_decimal_places=2,
        number_negative=False,
        order=3,
    )

    handler = RowHandler()

    rows, report = handler.import_rows(
        user=user,
        table=table,
        data=[
            [
                "Tesla",
                240,
                59999.99,
            ],
            [
                "Giulietta",
                210,
                34999.99,
            ],
            [
                "Panda",
                160,
                8999.99,
            ],
        ],
        send_signal=False,
    )
    assert len(rows) == 3
    assert report == {}

    model = table.get_model()
    assert model.objects.count() == 3

    send_mock.assert_not_called()

    rows, report = handler.import_rows(
        user=user,
        table=table,
        data=[
            [
                "Tesla",
                240,
                59999.999999,
            ],
            [
                "Giulietta",
                210.888,
                34999.99,
            ],
            [
                "Panda",
                160,
                8999.99,
            ],
        ],
    )

    assert len(rows) == 1
    assert sorted(report.keys()) == sorted([0, 1])

    model = table.get_model()
    assert model.objects.count() == 4

    send_mock.assert_called_once()

    rows, report = handler.import_rows(
        user=user,
        table=table,
        data=[
            [
                "Panda",
                160,
                8999.99,
            ],
            ["Tesla", 240, 59999.999999, "bli bloup"],
            [
                "Giulietta",
                210.888,
            ],
        ],
    )

    assert len(rows) == 1
    assert sorted(report.keys()) == sorted([1, 2])


@pytest.mark.django_db
@patch("baserow.contrib.database.rows.signals.rows_updated.send")
@patch("baserow.contrib.database.rows.signals.before_rows_update.send")
def test_move_row(before_send_mock, send_mock, data_fixture):
    user = data_fixture.create_user()
    user_2 = data_fixture.create_user()
    table = data_fixture.create_database_table(name="Car", user=user)

    handler = RowHandler()
    row_1 = handler.create_row(user=user, table=table)
    row_2 = handler.create_row(user=user, table=table)
    row_3 = handler.create_row(user=user, table=table)

    with pytest.raises(UserNotInWorkspace):
        handler.move_row_by_id(user=user_2, table=table, row_id=row_1.id)

    with pytest.raises(RowDoesNotExist):
        handler.move_row_by_id(user=user, table=table, row_id=99999)

    handler.move_row_by_id(user=user, table=table, row_id=row_1.id)
    row_1.refresh_from_db()
    row_2.refresh_from_db()
    row_3.refresh_from_db()
    assert row_1.order == Decimal("4.00000000000000000000")
    assert row_2.order == Decimal("2.00000000000000000000")
    assert row_3.order == Decimal("3.00000000000000000000")

    before_send_mock.assert_called_once()
    assert before_send_mock.call_args[1]["rows"][0].id == row_1.id
    assert before_send_mock.call_args[1]["user"].id == user.id
    assert before_send_mock.call_args[1]["table"].id == table.id
    assert before_send_mock.call_args[1]["model"]._generated_table_model

    send_mock.assert_called_once()
    assert send_mock.call_args[1]["rows"][0].id == row_1.id
    assert send_mock.call_args[1]["user"].id == user.id
    assert send_mock.call_args[1]["table"].id == table.id
    assert send_mock.call_args[1]["model"]._generated_table_model
    assert send_mock.call_args[1]["before_return"] == before_send_mock.return_value

    handler.move_row_by_id(user=user, table=table, row_id=row_1.id, before_row=row_3)
    row_1.refresh_from_db()
    row_2.refresh_from_db()
    row_3.refresh_from_db()
    assert row_1.order == Decimal("2.50000000000000000000")
    assert row_2.order == Decimal("2.00000000000000000000")
    assert row_3.order == Decimal("3.00000000000000000000")

    row_ids = table.get_model().objects.all()
    assert row_ids[0].id == row_2.id
    assert row_ids[1].id == row_1.id
    assert row_ids[2].id == row_3.id


@pytest.mark.django_db
@patch("baserow.contrib.database.rows.signals.rows_deleted.send")
@patch("baserow.contrib.database.rows.signals.before_rows_delete.send")
def test_delete_row(before_send_mock, send_mock, data_fixture):
    user = data_fixture.create_user()
    user_2 = data_fixture.create_user()
    table = data_fixture.create_database_table(name="Car", user=user)
    data_fixture.create_text_field(table=table, name="Name", text_default="Test")

    handler = RowHandler()
    model = table.get_model()
    row = handler.create_row(user=user, table=table)
    handler.create_row(user=user, table=table)

    with pytest.raises(UserNotInWorkspace):
        handler.delete_row_by_id(user=user_2, table=table, row_id=row.id)

    with pytest.raises(RowDoesNotExist):
        handler.delete_row_by_id(user=user, table=table, row_id=99999)

    row_id = row.id
    handler.delete_row_by_id(user=user, table=table, row_id=row.id)
    assert model.objects.all().count() == 1
    assert model.trash.all().count() == 1
    row.refresh_from_db()
    assert row.trashed

    before_send_mock.assert_called_once()
    assert before_send_mock.call_args[1]["rows"]
    assert before_send_mock.call_args[1]["user"].id == user.id
    assert before_send_mock.call_args[1]["table"].id == table.id
    assert before_send_mock.call_args[1]["model"]._generated_table_model

    send_mock.assert_called_once()
    assert send_mock.call_args[1]["rows"][0].id == row_id
    assert send_mock.call_args[1]["user"].id == user.id
    assert send_mock.call_args[1]["table"].id == table.id
    assert send_mock.call_args[1]["model"]._generated_table_model
    assert send_mock.call_args[1]["before_return"] == before_send_mock.return_value


@pytest.mark.django_db
@patch("baserow.contrib.database.rows.signals.rows_created.send")
def test_restore_row(send_mock, data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(name="Car", user=user)
    name_field = data_fixture.create_text_field(
        table=table, name="Name", text_default="Test"
    )
    speed_field = data_fixture.create_number_field(
        table=table, name="Max speed", number_negative=True
    )
    price_field = data_fixture.create_number_field(
        table=table,
        name="Price",
        number_decimal_places=2,
        number_negative=False,
    )

    handler = RowHandler()

    row_1 = handler.create_row(
        user=user,
        table=table,
        values={
            name_field.id: "Tesla",
            speed_field.id: 240,
            f"field_{price_field.id}": 59999.99,
        },
    )

    handler.delete_row_by_id(user, table, row_1.id)
    TrashHandler.restore_item(user, "row", row_1.id, parent_trash_item_id=table.id)

    assert len(send_mock.call_args) == 2
    assert send_mock.call_args[1]["rows"][0].id == row_1.id
    assert send_mock.call_args[1]["user"] is None
    assert send_mock.call_args[1]["table"].id == table.id
    assert send_mock.call_args[1]["before"] is None
    assert send_mock.call_args[1]["model"]._generated_table_model


@pytest.mark.django_db
def test_get_include_exclude_fields_with_user_field_names(data_fixture):
    table = data_fixture.create_database_table()
    data_fixture.create_text_field(name="first", table=table, order=1)
    data_fixture.create_text_field(name="Test", table=table, order=2)
    data_fixture.create_text_field(name="Test_2", table=table, order=3)
    data_fixture.create_text_field(name="With Space", table=table, order=4)

    assert (
        get_include_exclude_fields(
            table, include=None, exclude=None, user_field_names=True
        )
        is None
    )

    assert (
        get_include_exclude_fields(table, include="", exclude="", user_field_names=True)
        is None
    )

    fields = get_include_exclude_fields(table, include="Test_2", user_field_names=True)
    assert list(fields.values_list("name", flat=True)) == ["Test_2"]

    fields = get_include_exclude_fields(
        table, "first,field_9999,Test", user_field_names=True
    )
    assert list(fields.values_list("name", flat=True)) == ["first", "Test"]

    fields = get_include_exclude_fields(
        table, None, "first,field_9999", user_field_names=True
    )
    assert list(fields.values_list("name", flat=True)) == [
        "Test",
        "Test_2",
        "With Space",
    ]

    fields = get_include_exclude_fields(
        table, "first,Test", "first", user_field_names=True
    )
    assert list(fields.values_list("name", flat=True)) == ["Test"]

    fields = get_include_exclude_fields(
        table, 'first,"With Space",Test', user_field_names=True
    )
    assert list(fields.values_list("name", flat=True)) == [
        "first",
        "Test",
        "With Space",
    ]


@pytest.mark.django_db
def test_has_row(data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(name="Car", user=user)
    name_field = data_fixture.create_text_field(
        table=table, name="Name", text_default="Test"
    )
    speed_field = data_fixture.create_number_field(
        table=table, name="Max speed", number_negative=True
    )
    price_field = data_fixture.create_number_field(
        table=table,
        name="Price",
        number_decimal_places=2,
        number_negative=False,
    )

    handler = RowHandler()
    row = handler.create_row(
        user=user,
        table=table,
        values={
            f"field_{name_field.id}": "Tesla",
            f"field_{speed_field.id}": 240,
            f"field_{price_field.id}": Decimal("59999.99"),
        },
    )

    with pytest.raises(RowDoesNotExist):
        handler.has_row(user=user, table=table, row_id=99999, raise_error=True)
    assert not handler.has_row(user=user, table=table, row_id=99999, raise_error=False)

    assert handler.has_row(user=user, table=table, row_id=row.id, raise_error=False)
    assert handler.has_row(user=user, table=table, row_id=row.id, raise_error=True)


@pytest.mark.django_db
def test_get_unique_orders_without_before_row(data_fixture):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user)
    table = data_fixture.create_database_table(
        name="Table", user=user, database=database
    )

    model = table.get_model()
    model.objects.create(order=Decimal("1.00000000000000000000"))
    model.objects.create(order=Decimal("2.00000000000000000000"))
    model.objects.create(order=Decimal("3.00000000000000000000"))
    model.objects.create(order=Decimal("4.00000000000000000000"))

    handler = RowHandler()
    assert handler.get_unique_orders_before_row(None, model) == [
        Decimal("5.00000000000000000000")
    ]
    assert handler.get_unique_orders_before_row(None, model, 3) == [
        Decimal("5.00000000000000000000"),
        Decimal("6.00000000000000000000"),
        Decimal("7.00000000000000000000"),
    ]


@pytest.mark.django_db
def test_get_unique_orders_with_before_row(data_fixture):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user)
    table = data_fixture.create_database_table(
        name="Table", user=user, database=database
    )

    model = table.get_model()
    model.objects.create(order=Decimal("1.00000000000000000000"))
    row_2 = model.objects.create(order=Decimal("2.00000000000000000000"))
    model.objects.create(order=Decimal("3.00000000000000000000"))
    row_4 = model.objects.create(order=Decimal("4.00000000000000000000"))

    handler = RowHandler()
    assert handler.get_unique_orders_before_row(row_2, model) == [
        Decimal("1.50000000000000000000")
    ]
    assert handler.get_unique_orders_before_row(row_2, model, 3) == [
        Decimal("1.5"),
        Decimal("1.66666666666666674068"),
        Decimal("1.75"),
    ]
    assert handler.get_unique_orders_before_row(row_4, model) == [
        Decimal("3.50000000000000000000")
    ]


@pytest.mark.django_db
def test_get_unique_orders_first_before_row(data_fixture):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user)
    table = data_fixture.create_database_table(
        name="Table", user=user, database=database
    )

    model = table.get_model()
    row_1 = model.objects.create(order=Decimal("1.00000000000000000000"))

    handler = RowHandler()
    assert handler.get_unique_orders_before_row(row_1, model) == [
        Decimal("0.50000000000000000000")
    ]
    assert handler.get_unique_orders_before_row(row_1, model, 3) == [
        Decimal("0.5"),
        Decimal("0.66666666666666662966"),
        Decimal("0.75"),
    ]


@pytest.mark.django_db
def test_get_unique_orders_before_row_triggering_full_table_order_reset(data_fixture):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user)
    table = data_fixture.create_database_table(
        name="Table", user=user, database=database
    )

    model = table.get_model()
    row_1 = model.objects.create(order=Decimal("1.00000000000000000000"))
    row_2 = model.objects.create(order=Decimal("1.00000000000000001000"))
    row_3 = model.objects.create(order=Decimal("2.99999999999999999999"))
    row_4 = model.objects.create(order=Decimal("2.99999999999999999998"))

    handler = RowHandler()
    assert handler.get_unique_orders_before_row(row_3, model, 2) == [
        Decimal("3.50000000000000000000"),
        Decimal("3.66666666666666651864"),
    ]

    row_1.refresh_from_db()
    row_2.refresh_from_db()
    row_3.refresh_from_db()
    row_4.refresh_from_db()

    assert row_1.order == Decimal("1.00000000000000000000")
    assert row_2.order == Decimal("2.00000000000000000000")
    assert row_3.order == Decimal("4.00000000000000000000")
    assert row_4.order == Decimal("3.00000000000000000000")


@pytest.mark.django_db
@patch("baserow.contrib.database.rows.signals.row_orders_recalculated.send")
def test_recalculate_row_orders(send_mock, data_fixture):
    database = data_fixture.create_database_application()
    table = data_fixture.create_database_table(database=database)
    model = table.get_model()

    row_1 = model.objects.create(order="1.99999999999999999999")
    row_2 = model.objects.create(order="2.00000000000000000000")
    row_3 = model.objects.create(order="1.99999999999999999999")
    row_4 = model.objects.create(order="2.10000000000000000000")
    row_5 = model.objects.create(order="3.00000000000000000000")
    row_6 = model.objects.create(order="1.00000000000000000001")
    row_7 = model.objects.create(order="3.99999999999999999999")
    row_8 = model.objects.create(order="4.00000000000000000001")

    RowHandler().recalculate_row_orders(table)

    rows = model.objects.all()
    assert rows[0].id == row_6.id
    assert rows[0].order == Decimal("1.00000000000000000000")

    assert rows[1].id == row_1.id
    assert rows[1].order == Decimal("2.00000000000000000000")

    assert rows[2].id == row_3.id
    assert rows[2].order == Decimal("3.00000000000000000000")

    assert rows[3].id == row_2.id
    assert rows[3].order == Decimal("4.00000000000000000000")

    assert rows[4].id == row_4.id
    assert rows[4].order == Decimal("5.00000000000000000000")

    assert rows[5].id == row_5.id
    assert rows[5].order == Decimal("6.00000000000000000000")

    assert rows[6].id == row_7.id
    assert rows[6].order == Decimal("7.00000000000000000000")

    assert rows[7].id == row_8.id
    assert rows[7].order == Decimal("8.00000000000000000000")

    send_mock.assert_called_once()
    assert send_mock.call_args[1]["table"].id == table.id
