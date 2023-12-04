import pytest

from baserow.contrib.database.api.views.serializers import serialize_group_by_meta_data
from baserow.contrib.database.fields.registries import field_type_registry
from baserow.contrib.database.views.handler import ViewHandler
from baserow.test_utils.helpers import setup_interesting_test_table


@pytest.mark.django_db
def test_serialize_group_by_meta_data(api_client, data_fixture):
    table = data_fixture.create_database_table()
    text_field = data_fixture.create_text_field(
        table=table, order=0, name="Color", text_default="white"
    )
    number_field = data_fixture.create_number_field(
        table=table,
        order=1,
        name="Horsepower",
        number_decimal_places=3,
    )

    model = table.get_model()
    model.objects.create(
        **{
            f"field_{text_field.id}": "Green",
            f"field_{number_field.id}": 10,
        }
    )
    model.objects.create(
        **{
            f"field_{text_field.id}": "Orange",
            f"field_{number_field.id}": 10,
        }
    )

    queryset = model.objects.all()
    rows = list(queryset)

    handler = ViewHandler()
    counts = handler.get_group_by_meta_data_in_rows(
        [text_field, number_field], rows, queryset
    )

    assert dict(serialize_group_by_meta_data(counts)) == {
        f"field_{text_field.id}": [
            {f"field_{text_field.id}": "Green", "count": 1},
            {f"field_{text_field.id}": "Orange", "count": 1},
        ],
        f"field_{number_field.id}": [
            {
                f"field_{text_field.id}": "Green",
                f"field_{number_field.id}": "10.000",
                "count": 1,
            },
            {
                f"field_{text_field.id}": "Orange",
                f"field_{number_field.id}": "10.000",
                "count": 1,
            },
        ],
    }


@pytest.mark.django_db
def test_serialize_group_by_meta_data_on_all_fields_in_interesting_table(
    api_client, data_fixture
):
    table, user, row, _, context = setup_interesting_test_table(data_fixture)
    model = table.get_model()
    queryset = model.objects.all()
    rows = list(queryset)
    handler = ViewHandler()
    all_fields = [field.specific for field in table.field_set.all()]
    fields_to_group_by = [
        field
        for field in all_fields
        if field_type_registry.get_by_model(field).check_can_group_by(field)
    ]

    actual_result_per_field_name = {}

    for field in fields_to_group_by:
        counts = handler.get_group_by_meta_data_in_rows([field], rows, queryset)
        serialized = serialize_group_by_meta_data(counts)[field.db_column]
        # rename the `field_{id}` to the field name, so that we can do an accurate
        # comparison.
        for result in serialized:
            result[f"field_{field.name}"] = result.pop(f"field_{str(field.id)}")
        actual_result_per_field_name[field.name] = serialized

    # Keep this manually in sync with `test/unit/database/fieldTypes.spec.js` "group
    # by values match the field type" test.
    assert actual_result_per_field_name == {
        "text": [
            {"count": 1, "field_text": "text"},
            {"count": 1, "field_text": None},
        ],
        "long_text": [
            {"count": 1, "field_long_text": "long_text"},
            {"count": 1, "field_long_text": None},
        ],
        "url": [
            {"count": 1, "field_url": ""},
            {"count": 1, "field_url": "https://www.google.com"},
        ],
        "email": [
            {"count": 1, "field_email": ""},
            {"count": 1, "field_email": "test@example.com"},
        ],
        "negative_int": [
            {"count": 1, "field_negative_int": "-1"},
            {"count": 1, "field_negative_int": None},
        ],
        "positive_int": [
            {"count": 1, "field_positive_int": "1"},
            {"count": 1, "field_positive_int": None},
        ],
        "negative_decimal": [
            {"count": 1, "field_negative_decimal": "-1.2"},
            {"count": 1, "field_negative_decimal": None},
        ],
        "positive_decimal": [
            {"count": 1, "field_positive_decimal": "1.2"},
            {"count": 1, "field_positive_decimal": None},
        ],
        "rating": [{"count": 1, "field_rating": 0}, {"count": 1, "field_rating": 3}],
        "boolean": [
            {"count": 1, "field_boolean": False},
            {"count": 1, "field_boolean": True},
        ],
        "datetime_us": [
            {"count": 1, "field_datetime_us": "2020-02-01T01:23:00Z"},
            {"count": 1, "field_datetime_us": None},
        ],
        "date_us": [
            {"count": 1, "field_date_us": "2020-02-01"},
            {"count": 1, "field_date_us": None},
        ],
        "datetime_eu": [
            {"count": 1, "field_datetime_eu": "2020-02-01T01:23:00Z"},
            {"count": 1, "field_datetime_eu": None},
        ],
        "date_eu": [
            {"count": 1, "field_date_eu": "2020-02-01"},
            {"count": 1, "field_date_eu": None},
        ],
        "datetime_eu_tzone_visible": [
            {"count": 1, "field_datetime_eu_tzone_visible": "2020-02-01T01:23:00Z"},
            {"count": 1, "field_datetime_eu_tzone_visible": None},
        ],
        "datetime_eu_tzone_hidden": [
            {"count": 1, "field_datetime_eu_tzone_hidden": "2020-02-01T01:23:00Z"},
            {"count": 1, "field_datetime_eu_tzone_hidden": None},
        ],
        "last_modified_datetime_us": [
            {"count": 2, "field_last_modified_datetime_us": "2021-01-02T12:00:00Z"}
        ],
        "last_modified_date_us": [
            {"count": 2, "field_last_modified_date_us": "2021-01-02"}
        ],
        "last_modified_datetime_eu": [
            {"count": 2, "field_last_modified_datetime_eu": "2021-01-02T12:00:00Z"}
        ],
        "last_modified_date_eu": [
            {"count": 2, "field_last_modified_date_eu": "2021-01-02"}
        ],
        "last_modified_datetime_eu_tzone": [
            {
                "count": 2,
                "field_last_modified_datetime_eu_tzone": "2021-01-02T12:00:00Z",
            }
        ],
        "created_on_datetime_us": [
            {"count": 2, "field_created_on_datetime_us": "2021-01-02T12:00:00Z"}
        ],
        "created_on_date_us": [{"count": 2, "field_created_on_date_us": "2021-01-02"}],
        "created_on_datetime_eu": [
            {"count": 2, "field_created_on_datetime_eu": "2021-01-02T12:00:00Z"}
        ],
        "created_on_date_eu": [{"count": 2, "field_created_on_date_eu": "2021-01-02"}],
        "created_on_datetime_eu_tzone": [
            {"count": 2, "field_created_on_datetime_eu_tzone": "2021-01-02T12:00:00Z"}
        ],
        "single_select": [
            {"count": 1, "field_single_select": 1},
            {"count": 1, "field_single_select": None},
        ],
        "multiple_select": [
            {"count": 1, "field_multiple_select": ""},
            {"count": 1, "field_multiple_select": "4,3,5"},
        ],
        "phone_number": [
            {"count": 1, "field_phone_number": ""},
            {"count": 1, "field_phone_number": "+4412345678"},
        ],
        "formula_text": [{"count": 2, "field_formula_text": "test FORMULA"}],
        "formula_int": [{"count": 2, "field_formula_int": "1"}],
        "formula_bool": [{"count": 2, "field_formula_bool": True}],
        "formula_decimal": [{"count": 2, "field_formula_decimal": "33.3333333333"}],
        "formula_dateinterval": [{"count": 2, "field_formula_dateinterval": "1 day"}],
        "formula_date": [{"count": 2, "field_formula_date": "2020-01-01"}],
        "formula_email": [
            {"count": 1, "field_formula_email": ""},
            {"count": 1, "field_formula_email": "test@example.com"},
        ],
        "count": [{"count": 1, "field_count": "0"}, {"count": 1, "field_count": "3"}],
        "rollup": [
            {"count": 1, "field_rollup": "-122.222"},
            {"count": 1, "field_rollup": "0.000"},
        ],
    }
