import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK

from baserow.contrib.builder.workflow_actions.workflow_action_types import (
    NotificationWorkflowActionType,
)


@pytest.mark.django_db
def test_create_workflow_action(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    workflow_action_type = NotificationWorkflowActionType.type

    url = reverse("api:builder:workflow_action:list", kwargs={"page_id": page.id})
    response = api_client.post(
        url,
        {"type": workflow_action_type, "event": "click"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["type"] == workflow_action_type


@pytest.mark.django_db
def test_get_workflow_actions(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    workflow_action_one = data_fixture.create_notification_workflow_action(page=page)
    workflow_action_two = data_fixture.create_notification_workflow_action(page=page)

    url = reverse("api:builder:workflow_action:list", kwargs={"page_id": page.id})
    response = api_client.get(
        url,
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(response_json) == 2
    assert response_json[0]["id"] == workflow_action_one.id
    assert response_json[1]["id"] == workflow_action_two.id
