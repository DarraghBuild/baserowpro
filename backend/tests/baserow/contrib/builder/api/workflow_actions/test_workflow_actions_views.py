import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK

from baserow.contrib.builder.workflow_actions.workflow_action_types import (
    NotificationWorkflowActionType,
)


@pytest.mark.django_db
def test_create_workflow_action(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    element = data_fixture.create_builder_button_element(user=user)
    workflow_action_type = NotificationWorkflowActionType.type

    url = reverse("api:builder:workflow_action:list", kwargs={"element_id": element.id})
    response = api_client.post(
        url,
        {"type": workflow_action_type},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["type"] == workflow_action_type
