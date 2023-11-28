import pytest
from rest_framework.exceptions import ValidationError

from baserow.contrib.builder.workflow_actions.models import EventTypes
from baserow.contrib.builder.workflow_actions.registries import (
    builder_workflow_action_type_registry,
)
from baserow.contrib.builder.workflow_actions.workflow_action_types import (
    UpsertRowWorkflowActionType,
)
from baserow.core.services.models import Service
from baserow.core.workflow_actions.registries import WorkflowActionType


def pytest_generate_tests(metafunc):
    if "workflow_action_type" in metafunc.fixturenames:
        metafunc.parametrize(
            "workflow_action_type",
            [
                pytest.param(e, id=e.type)
                for e in builder_workflow_action_type_registry.get_all()
            ],
        )


@pytest.mark.django_db
def test_export_workflow_action(data_fixture, workflow_action_type: WorkflowActionType):
    page = data_fixture.create_builder_page()
    pytest_params = workflow_action_type.get_pytest_params(data_fixture)
    workflow_action = data_fixture.create_workflow_action(
        workflow_action_type.model_class, page=page, **pytest_params
    )

    exported = workflow_action_type.export_serialized(workflow_action)

    assert exported["id"] == workflow_action.id
    assert exported["type"] == workflow_action_type.type

    for key, value in pytest_params.items():
        assert exported[key] == value


@pytest.mark.django_db
def test_import_workflow_action(data_fixture, workflow_action_type: WorkflowActionType):
    page = data_fixture.create_builder_page()
    pytest_params = workflow_action_type.get_pytest_params(data_fixture)

    page_after_import = data_fixture.create_builder_page()

    serialized = {
        "id": 9999,
        "type": workflow_action_type.type,
        "page_id": page.id,
        "order": 0,
    }
    serialized.update(pytest_params)

    id_mapping = {"builder_pages": {page.id: page_after_import.id}}
    workflow_action = workflow_action_type.import_serialized(
        page, serialized, id_mapping
    )

    assert workflow_action.id != 9999
    assert isinstance(workflow_action, workflow_action_type.model_class)

    for key, value in pytest_params.items():
        assert getattr(workflow_action, key) == value


@pytest.mark.django_db
def test_upsert_row_workflow_action_type_prepare_value_for_db(data_fixture):
    with pytest.raises(ValidationError):
        UpsertRowWorkflowActionType().prepare_value_for_db(
            {"table_id": 9999999999999999}
        )
    with pytest.raises(ValidationError):
        UpsertRowWorkflowActionType().prepare_value_for_db(
            {"integration_id": 9999999999999999}
        )

    table = data_fixture.create_database_table()
    field = data_fixture.create_text_field(table=table)
    values = UpsertRowWorkflowActionType().prepare_value_for_db(
        {
            "table_id": table.id,
            "field_mappings": [{"field_id": field.id, "value": "'Bread'"}],
        }
    )
    service = Service.objects.get(pk=values["service_id"]).specific
    mapping = service.field_mappings.get()
    assert mapping.field_id == field.id
    assert mapping.value == "'Bread'"

    # Set a new table with `table2`, but use `field` from `table`
    table2 = data_fixture.create_database_table()
    with pytest.raises(ValidationError):
        UpsertRowWorkflowActionType().prepare_value_for_db(
            {
                "table_id": table2.id,
                "field_mappings": [{"field_id": field.id, "value": "'Bread'"}],
            }
        )


@pytest.mark.django_db
def test_upsert_row_workflow_action_type_prepare_value_for_db_without_instance(
    data_fixture,
):
    page = data_fixture.create_builder_page()
    integration = data_fixture.create_local_baserow_integration(
        application=page.builder
    )
    table = data_fixture.create_database_table()
    field = data_fixture.create_text_field(table=table)
    model = table.get_model()
    row = model.objects.create(**{f"field_{field.id}": "Cheese"})
    values = UpsertRowWorkflowActionType().prepare_value_for_db(
        {"row_id": row.id, "table_id": table.id, "integration_id": integration.id}
    )
    service = Service.objects.get(pk=values["service_id"]).specific
    assert service.row_id == str(row.id)
    assert service.table_id == table.id
    assert service.integration_id == integration.id


@pytest.mark.django_db
def test_upsert_row_workflow_action_type_prepare_value_for_db_with_instance(
    data_fixture,
):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    element = data_fixture.create_builder_button_element(page=page)
    integration = data_fixture.create_local_baserow_integration(
        application=page.builder
    )
    workflow_action = data_fixture.create_local_baserow_create_row_workflow_action(
        page=page, element=element, event=EventTypes.CLICK, user=user
    )
    table2 = data_fixture.create_database_table()
    field2 = data_fixture.create_text_field(table=table2)
    model2 = table2.get_model()
    row2 = model2.objects.create(**{f"field_{field2.id}": "Cheese"})
    values = UpsertRowWorkflowActionType().prepare_value_for_db(
        {
            "row_id": row2.id,
            "table_id": table2.id,
            "integration_id": integration.id,
        },
        instance=workflow_action,
    )
    service = Service.objects.get(pk=values["service_id"]).specific
    assert service.row_id == str(row2.id)
    assert service.table_id == table2.id
    assert service.integration_id == integration.id
