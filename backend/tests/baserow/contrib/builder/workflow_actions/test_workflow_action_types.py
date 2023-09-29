import pytest

from baserow.contrib.builder.workflow_actions.registries import (
    builder_workflow_action_type_registry,
)
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
    sample_params = workflow_action_type.get_sample_params()
    workflow_action = data_fixture.create_workflow_action(
        workflow_action_type.model_class, page=page, **sample_params
    )

    exported = workflow_action_type.export_serialized(workflow_action)

    assert exported["id"] == workflow_action.id
    assert exported["type"] == workflow_action_type.type

    for key, value in sample_params.items():
        assert exported[key] == value
