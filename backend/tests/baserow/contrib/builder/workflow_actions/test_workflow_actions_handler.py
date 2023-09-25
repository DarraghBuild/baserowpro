"""
TODO: we should move this into core once we have workflow actions that are defined in
    core
"""
import pytest

from baserow.contrib.builder.workflow_actions.models import (
    EventTypes,
    BuilderWorkflowAction,
)
from baserow.contrib.builder.workflow_actions.workflow_action_types import (
    NotificationWorkflowActionType,
)
from baserow.core.workflow_actions.handler import WorkflowActionHandler


@pytest.mark.django_db
def test_create_workflow_action(data_fixture):
    element = data_fixture.create_builder_button_element()
    event = EventTypes.CLICK
    workflow_action_type = NotificationWorkflowActionType()
    workflow_action = (
        WorkflowActionHandler()
        .create_workflow_action(workflow_action_type, element=element, event=event)
        .specific
    )

    assert workflow_action is not None
    assert workflow_action.element is element
    assert BuilderWorkflowAction.objects.count() == 1


@pytest.mark.django_db
def test_delete_workflow_action(data_fixture):
    element = data_fixture.create_builder_button_element()
    event = EventTypes.CLICK
    workflow_action = data_fixture.create_notification_workflow_action(
        element=element, event=event
    )

    assert BuilderWorkflowAction.objects.count() == 1

    WorkflowActionHandler().delete_workflow_action(workflow_action)

    assert BuilderWorkflowAction.objects.count() == 0


@pytest.mark.django_db
def test_update_workflow_action(data_fixture):
    element = data_fixture.create_builder_button_element()
    event = EventTypes.CLICK
    workflow_action = data_fixture.create_notification_workflow_action(
        element=element, event=event
    )

    element_changed = data_fixture.create_builder_button_element()

    workflow_action = WorkflowActionHandler().update_workflow_action(
        workflow_action, element=element_changed
    )

    workflow_action.refresh_from_db()
    assert workflow_action.element_id == element_changed.id
