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

    assert serialize_group_by_meta_data(counts) == {
        f"field_{text_field.id}": [
            {"field_1": "Green", "count": 1},
            {"field_1": "Orange", "count": 1},
        ],
        f"field_{number_field.id}": [
            {"field_1": "Green", "field_2": "10.000", "count": 1},
            {"field_1": "Orange", "field_2": "10.000", "count": 1},
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
        actual_result_per_field_name[field.name] = serialize_group_by_meta_data(counts)[
            field.db_column
        ]

    assert actual_result_per_field_name == {
        "text": [{"count": 1, "field_4": "text"}, {"count": 1, "field_4": "None"}],
        "long_text": [
            {"count": 1, "field_5": "long_text"},
            {"count": 1, "field_5": "None"},
        ],
        "url": [
            {"count": 1, "field_6": ""},
            {"count": 1, "field_6": "https://www.google.com"},
        ],
        "email": [
            {"count": 1, "field_7": ""},
            {"count": 1, "field_7": "test@example.com"},
        ],
        "negative_int": [{"count": 1, "field_8": "-1"}, {"count": 1, "field_8": ""}],
        "positive_int": [{"count": 1, "field_9": "1"}, {"count": 1, "field_9": ""}],
        "negative_decimal": [
            {"count": 1, "field_10": "-1.2"},
            {"count": 1, "field_10": ""},
        ],
        "positive_decimal": [
            {"count": 1, "field_11": "1.2"},
            {"count": 1, "field_11": ""},
        ],
        "rating": [{"count": 1, "field_12": 0}, {"count": 1, "field_12": 3}],
        "boolean": [{"count": 1, "field_13": False}, {"count": 1, "field_13": True}],
        "datetime_us": [
            {"count": 1, "field_14": "2020-02-01T01:23:00Z"},
            {"count": 1, "field_14": None},
        ],
        "date_us": [
            {"count": 1, "field_15": "2020-02-01"},
            {"count": 1, "field_15": None},
        ],
        "datetime_eu": [
            {"count": 1, "field_16": "2020-02-01T01:23:00Z"},
            {"count": 1, "field_16": None},
        ],
        "date_eu": [
            {"count": 1, "field_17": "2020-02-01"},
            {"count": 1, "field_17": None},
        ],
        "datetime_eu_tzone_visible": [
            {"count": 1, "field_18": "2020-02-01T01:23:00Z"},
            {"count": 1, "field_18": None},
        ],
        "datetime_eu_tzone_hidden": [
            {"count": 1, "field_19": "2020-02-01T01:23:00Z"},
            {"count": 1, "field_19": None},
        ],
        "last_modified_datetime_us": [{"count": 2, "field_20": "2021-01-02T12:00:00Z"}],
        "last_modified_date_us": [{"count": 2, "field_21": "2021-01-02"}],
        "last_modified_datetime_eu": [{"count": 2, "field_22": "2021-01-02T12:00:00Z"}],
        "last_modified_date_eu": [{"count": 2, "field_23": "2021-01-02"}],
        "last_modified_datetime_eu_tzone": [
            {"count": 2, "field_24": "2021-01-02T12:00:00Z"}
        ],
        "created_on_datetime_us": [{"count": 2, "field_25": "2021-01-02T12:00:00Z"}],
        "created_on_date_us": [{"count": 2, "field_26": "2021-01-02"}],
        "created_on_datetime_eu": [{"count": 2, "field_27": "2021-01-02T12:00:00Z"}],
        "created_on_date_eu": [{"count": 2, "field_28": "2021-01-02"}],
        "created_on_datetime_eu_tzone": [
            {"count": 2, "field_29": "2021-01-02T12:00:00Z"}
        ],
        "single_select": [{"count": 1, "field_40": 1}, {"count": 1, "field_40": None}],
        "multiple_select": [
            {"count": 1, "field_41": ""},
            {"count": 1, "field_41": "4,3,5"},
        ],
        "phone_number": [
            {"count": 1, "field_43": ""},
            {"count": 1, "field_43": "+4412345678"},
        ],
        "formula_text": [{"count": 2, "field_44": "test FORMULA"}],
        "formula_int": [{"count": 2, "field_45": "1"}],
        "formula_bool": [{"count": 2, "field_46": True}],
        "formula_decimal": [{"count": 2, "field_47": "33.3333333333"}],
        "formula_dateinterval": [{"count": 2, "field_48": "1 day"}],
        "formula_date": [{"count": 2, "field_49": "2020-01-01"}],
        "formula_email": [
            {"count": 1, "field_51": ""},
            {"count": 1, "field_51": "test@example.com"},
        ],
        "count": [{"count": 1, "field_54": "0"}, {"count": 1, "field_54": "3"}],
        "rollup": [
            {"count": 1, "field_55": "-122.222"},
            {"count": 1, "field_55": "0.000"},
        ],
    }
