from datetime import timedelta

import pytest

from baserow.contrib.database.fields.handler import FieldHandler
from baserow.contrib.database.fields.registries import field_type_registry
from baserow.contrib.database.rows.handler import RowHandler

# TODO: test create duration field, update it, create rows with it, deleting it
# TODO: CRUD rows with duration field


@pytest.mark.field_duration
@pytest.mark.django_db
def test_duration_field_type_default_format(data_fixture):
    user = data_fixture.create_user()
    table = data_fixture.create_database_table(user=user)

    field_handler = FieldHandler()
    field = field_handler.create_field(
        user=user,
        table=table,
        type_name="duration",
        name="duration",
    )

    assert field.duration_format == "h:mm"


# TODO: test some incorrect values as well
@pytest.mark.parametrize(
    "duration_format,user_input,new_text_field_value",
    [
        (
            "h:mm",
            timedelta(seconds=3660),
            "1:01",
        ),
        (
            "h:mm:ss",
            timedelta(seconds=3665),
            "1:01:05",
        ),
        (
            "h:mm:ss.s",
            timedelta(seconds=3665.5),
            "1:01:05.5",
        ),
        (
            "h:mm:ss.ss",
            timedelta(seconds=3665.55),
            "1:01:05.55",
        ),
        (
            "h:mm:ss.sss",
            timedelta(seconds=3665.555),
            "1:01:05.555",
        ),
    ],
)
@pytest.mark.django_db
def test_convert_duration_field_to_text_field(
    data_fixture,
    duration_format,
    user_input,
    new_text_field_value,
):
    user = data_fixture.create_user()
    workspace = data_fixture.create_workspace(user=user)
    database = data_fixture.create_database_application(workspace=workspace)
    table = data_fixture.create_database_table(database=database)
    field_handler = FieldHandler()
    row_handler = RowHandler()

    field = field_handler.create_field(
        user=user,
        table=table,
        name="Duration",
        type_name="duration",
        duration_format=duration_format,
    )

    row_handler.create_row(
        user=user,
        table=table,
        values={
            f"field_{field.id}": user_input,
        },
    )

    field_handler.update_field(
        user=user,
        field=field,
        new_type_name="text",
    )

    field_type = field_type_registry.get_by_model(field)
    model = table.get_model()

    table_models = model.objects.all()
    assert table_models.count() == 1
    table_model = table_models.first()
    updated_value = getattr(table_model, f"field_{field.id}")
    assert updated_value == new_text_field_value


# TODO: test some incorrect values as well
@pytest.mark.parametrize(
    "duration_format,text_field_value,new_duration_field_value",
    [
        (
            "h:mm",
            "1:01",
            timedelta(seconds=3660),
        ),
        (
            "h:mm:ss",
            "1:01:05",
            timedelta(seconds=3665),
        ),
        (
            "h:mm:ss.s",
            "1:01:05.5",
            timedelta(seconds=3665.5),
        ),
        (
            "h:mm:ss.ss",
            "1:01:05.55",
            timedelta(seconds=3665.55),
        ),
        (
            "h:mm:ss.sss",
            "1:01:05.555",
            timedelta(seconds=3665.555),
        ),
    ],
)
@pytest.mark.django_db
def test_convert_text_field_to_duration_field(
    data_fixture,
    duration_format,
    text_field_value,
    new_duration_field_value,
):
    user = data_fixture.create_user()
    workspace = data_fixture.create_workspace(user=user)
    database = data_fixture.create_database_application(workspace=workspace)
    table = data_fixture.create_database_table(database=database)
    field_handler = FieldHandler()
    row_handler = RowHandler()

    field = field_handler.create_field(
        user=user,
        table=table,
        name="Text",
        type_name="text",
    )

    row_handler.create_row(
        user=user,
        table=table,
        values={
            f"field_{field.id}": text_field_value,
        },
    )

    field_handler.update_field(
        user=user,
        field=field,
        new_type_name="duration",
        duration_format=duration_format,
    )

    field_type = field_type_registry.get_by_model(field)
    model = table.get_model()

    table_models = model.objects.all()
    assert table_models.count() == 1
    table_model = table_models.first()
    updated_value = getattr(table_model, f"field_{field.id}")

    assert updated_value == new_duration_field_value
