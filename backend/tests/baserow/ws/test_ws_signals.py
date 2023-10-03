from datetime import timedelta
from unittest.mock import patch

from django.db import transaction
from django.utils import timezone

import pytest

from baserow.core.handler import CoreHandler
from baserow.core.models import (
    WORKSPACE_USER_PERMISSION_ADMIN,
    WORKSPACE_USER_PERMISSION_MEMBER,
)
from baserow.core.trash.handler import TrashHandler
from baserow.core.user.handler import UserHandler
from baserow.core.utils import generate_hash


@pytest.mark.django_db(transaction=True)
@patch("baserow.ws.signals.broadcast_to_group")
@patch("baserow.ws.signals.broadcast_to_groups")
@pytest.mark.websockets
def test_user_updated_name(
    mock_broadcast_to_workspaces, mock_broadcast_to_workspace, data_fixture
):
    user = data_fixture.create_user(first_name="Albert")
    workspace_user = CoreHandler().create_workspace(user=user, name="Test")
    workspace_user_2 = CoreHandler().create_workspace(user=user, name="Test 2")

    UserHandler().update_user(user, first_name="Jack")

    mock_broadcast_to_workspaces.delay.assert_called_once()
    args = mock_broadcast_to_workspaces.delay.call_args
    assert args[0][0] == [workspace_user.workspace.id, workspace_user_2.workspace.id]
    assert args[0][1]["type"] == "user_updated"
    assert args[0][1]["user"]["id"] == user.id
    assert args[0][1]["user"]["first_name"] == "Jack"


@pytest.mark.django_db(transaction=True)
@patch("baserow.ws.signals.broadcast_to_group")
@patch("baserow.ws.signals.broadcast_to_groups")
@pytest.mark.websockets
def test_schedule_user_deletion(
    mock_broadcast_to_workspaces, mock_broadcast_to_workspace, data_fixture
):
    user = data_fixture.create_user(first_name="Albert", password="albert")
    workspace_user = CoreHandler().create_workspace(user=user, name="Test")
    workspace_user_2 = CoreHandler().create_workspace(user=user, name="Test 2")

    UserHandler().schedule_user_deletion(user)

    mock_broadcast_to_workspaces.delay.assert_called_once()
    args = mock_broadcast_to_workspaces.delay.call_args
    assert args[0][0] == [workspace_user.workspace.id, workspace_user_2.workspace.id]
    assert args[0][1]["type"] == "user_deleted"
    assert args[0][1]["user"]["id"] == user.id


@pytest.mark.django_db(transaction=True)
@patch("baserow.ws.signals.broadcast_to_group")
@patch("baserow.ws.signals.broadcast_to_groups")
@pytest.mark.websockets
def test_cancel_user_deletion(
    mock_broadcast_to_workspaces, mock_broadcast_to_workspace, data_fixture
):
    user = data_fixture.create_user(first_name="Albert", password="albert")
    user.profile.to_be_deleted = True
    user.save()
    workspace_user = CoreHandler().create_workspace(user=user, name="Test")
    workspace_user_2 = CoreHandler().create_workspace(user=user, name="Test 2")

    UserHandler().cancel_user_deletion(user)

    mock_broadcast_to_workspaces.delay.assert_called_once()
    args = mock_broadcast_to_workspaces.delay.call_args
    assert args[0][0] == [workspace_user.workspace.id, workspace_user_2.workspace.id]
    assert args[0][1]["type"] == "user_restored"
    assert args[0][1]["user"]["id"] == user.id


@pytest.mark.django_db(transaction=True)
@patch("baserow.ws.signals.broadcast_to_group")
@patch("baserow.ws.signals.broadcast_to_groups")
@pytest.mark.websockets
def test_user_permanently_deleted(
    mock_broadcast_to_workspaces, mock_broadcast_to_workspace, data_fixture
):
    user = data_fixture.create_user(first_name="Albert", password="albert")
    user.profile.to_be_deleted = True
    user.profile.save()
    user.last_login = timezone.now() - timedelta(weeks=100)
    user.save()
    workspace_user = CoreHandler().create_workspace(user=user, name="Test")
    workspace_user_2 = CoreHandler().create_workspace(user=user, name="Test 2")

    UserHandler().delete_expired_users_and_related_workspaces_if_last_admin(
        grace_delay=timedelta(days=1)
    )

    mock_broadcast_to_workspaces.delay.assert_called_once()
    args = mock_broadcast_to_workspaces.delay.call_args
    assert args[0][0] == [workspace_user.workspace.id, workspace_user_2.workspace.id]
    assert args[0][1]["type"] == "user_permanently_deleted"
    assert args[0][1]["user_id"] == user.id


@pytest.mark.django_db(transaction=True)
@patch("baserow.ws.signals.broadcast_to_group")
@pytest.mark.websockets
def test_workspace_created(mock_broadcast_to_workspace, data_fixture):
    user = data_fixture.create_user()
    workspace_user = CoreHandler().create_workspace(user=user, name="Test")

    mock_broadcast_to_workspace.delay.assert_called_once()
    args = mock_broadcast_to_workspace.delay.call_args
    assert args[0][0] == workspace_user.workspace_id
    assert args[0][1]["type"] == "group_created"
    assert args[0][1]["group"]["id"] == workspace_user.workspace_id  # GroupDeprecation
    assert args[0][1]["workspace"]["id"] == workspace_user.workspace_id


@pytest.mark.django_db(transaction=True)
@patch("baserow.ws.signals.broadcast_to_users")
@pytest.mark.websockets
def test_workspace_restored(mock_broadcast_to_users, data_fixture):
    user = data_fixture.create_user()
    member_user = data_fixture.create_user()
    # This user should not be sent the restore signal
    data_fixture.create_user()
    workspace = data_fixture.create_workspace()
    workspace_user = data_fixture.create_user_workspace(
        user=user, workspace=workspace, permissions=WORKSPACE_USER_PERMISSION_ADMIN
    )
    member_workspace_user = data_fixture.create_user_workspace(
        user=member_user,
        workspace=workspace,
        permissions=WORKSPACE_USER_PERMISSION_MEMBER,
    )
    database = data_fixture.create_database_application(user=user, workspace=workspace)
    TrashHandler.trash(user, workspace, None, workspace)

    TrashHandler.restore_item(user, "workspace", workspace.id)

    args = mock_broadcast_to_users.delay.call_args_list
    assert len(args) == 2
    member_call = args[1][0]
    admin_call = args[0][0]
    assert member_call[0] == [member_user.id]
    assert member_call[1]["type"] == "group_restored"
    # GroupDeprecation
    assert member_call[1]["group"]["id"] == member_workspace_user.workspace_id
    assert member_call[1]["group"]["permissions"] == "MEMBER"
    assert member_call[1]["workspace"]["id"] == member_workspace_user.workspace_id
    assert member_call[1]["workspace"]["permissions"] == "MEMBER"
    expected_workspace_json = {
        "id": database.id,
        "name": database.name,
        "order": 0,
        "type": "database",
        "group": {"id": workspace.id, "name": workspace.name},  # GroupDeprecation
        "workspace": {"id": workspace.id, "name": workspace.name},
        "tables": [],
    }
    assert member_call[1]["applications"] == [expected_workspace_json]
    assert admin_call[0] == [user.id]
    assert admin_call[1]["type"] == "group_restored"
    # GroupDeprecation
    assert admin_call[1]["group"]["id"] == workspace_user.workspace_id
    assert admin_call[1]["group"]["permissions"] == "ADMIN"
    assert admin_call[1]["group"]["id"] == workspace_user.workspace_id
    assert admin_call[1]["workspace"]["id"] == workspace_user.workspace_id
    assert admin_call[1]["workspace"]["permissions"] == "ADMIN"
    assert admin_call[1]["workspace"]["id"] == workspace_user.workspace_id
    assert admin_call[1]["applications"] == [expected_workspace_json]


@pytest.mark.django_db(transaction=True)
@patch("baserow.ws.signals.broadcast_to_group")
@pytest.mark.websockets
def test_workspace_updated(mock_broadcast_to_workspace, data_fixture):
    user = data_fixture.create_user()
    user.web_socket_id = "test"
    workspace = data_fixture.create_workspace(user=user)
    with transaction.atomic():
        workspace = CoreHandler().get_workspace_for_update(workspace.id)
        workspace = CoreHandler().update_workspace(
            user=user, workspace=workspace, name="Test"
        )

    mock_broadcast_to_workspace.delay.assert_called_once()
    args = mock_broadcast_to_workspace.delay.call_args
    assert args[0][0] == workspace.id
    assert args[0][1]["type"] == "group_updated"
    assert args[0][1]["group_id"] == workspace.id  # GroupDeprecation
    assert args[0][1]["group"]["id"] == workspace.id  # GroupDeprecation
    assert args[0][1]["workspace_id"] == workspace.id
    assert args[0][1]["workspace"]["id"] == workspace.id
    assert args[0][2] == "test"


@pytest.mark.django_db(transaction=True)
@patch("baserow.ws.signals.broadcast_to_users")
@pytest.mark.websockets
def test_workspace_deleted(mock_broadcast_to_users, data_fixture):
    user = data_fixture.create_user()
    workspace = data_fixture.create_workspace(user=user)
    workspace_id = workspace.id
    with transaction.atomic():
        workspace = CoreHandler().get_workspace_for_update(workspace_id)
        CoreHandler().delete_workspace(user=user, workspace=workspace)

    mock_broadcast_to_users.delay.assert_called_once()
    args = mock_broadcast_to_users.delay.call_args
    assert args[0][0] == [user.id]
    assert args[0][1]["type"] == "group_deleted"
    assert args[0][1]["group_id"] == workspace_id  # GroupDeprecation
    assert args[0][1]["workspace_id"] == workspace_id


@pytest.mark.django_db(transaction=True)
@patch("baserow.core.notifications.receivers.broadcast_to_users")
@patch("baserow.ws.signals.broadcast_to_users")
@patch("baserow.ws.signals.broadcast_to_group")
@pytest.mark.websockets
def test_workspace_user_added(
    mock_broadcast_to_workspace,
    mock_broadcast_to_users,
    mock_broadcast_to_users2,
    data_fixture,
):
    user_1 = data_fixture.create_user()
    user_2 = data_fixture.create_user()
    workspace = data_fixture.create_workspace()
    workspace_user_1 = data_fixture.create_user_workspace(
        user=user_1, workspace=workspace
    )
    workspace_invitation = data_fixture.create_workspace_invitation(
        email=user_2.email, permissions="MEMBER", workspace=workspace
    )

    workspace_user_2 = CoreHandler().accept_workspace_invitation(
        user_2, workspace_invitation
    )

    mock_broadcast_to_workspace.delay.assert_called_once()
    args = mock_broadcast_to_workspace.delay.call_args
    assert args[0][0] == workspace.id
    assert args[0][1]["type"] == "group_user_added"
    assert args[0][1]["id"] == workspace_user_2.id
    assert args[0][1]["group_id"] == workspace.id  # GroupDeprecation
    assert (
        args[0][1]["group_user"]["user_id"] == workspace_user_2.user_id
    )  # GroupDeprecation
    assert args[0][1]["group_user"]["permissions"] == "MEMBER"  # GroupDeprecation
    assert args[0][1]["workspace_id"] == workspace.id
    assert args[0][1]["workspace_user"]["user_id"] == workspace_user_2.user_id
    assert args[0][1]["workspace_user"]["permissions"] == "MEMBER"


@pytest.mark.django_db(transaction=True)
@patch("baserow_enterprise.role.receivers.broadcast_to_users")
@patch("baserow.ws.signals.broadcast_to_group")
@pytest.mark.websockets
def test_workspace_user_updated(
    mock_broadcast_to_workspace, mock_broadcast_to_users, data_fixture
):
    user_1 = data_fixture.create_user()
    user_2 = data_fixture.create_user()
    workspace = data_fixture.create_workspace()
    workspace_user_1 = data_fixture.create_user_workspace(
        user=user_1, workspace=workspace
    )
    data_fixture.create_user_workspace(user=user_2, workspace=workspace)
    CoreHandler().update_workspace_user(
        user=user_2, workspace_user=workspace_user_1, permissions="MEMBER"
    )

    mock_broadcast_to_workspace.delay.assert_called_once()
    args = mock_broadcast_to_workspace.delay.call_args
    assert args[0][0] == workspace.id
    assert args[0][1]["type"] == "group_user_updated"
    assert args[0][1]["id"] == workspace_user_1.id
    assert args[0][1]["group_id"] == workspace.id  # GroupDeprecation
    assert (
        args[0][1]["group_user"]["user_id"] == workspace_user_1.user_id
    )  # GroupDeprecation
    assert args[0][1]["group_user"]["permissions"] == "MEMBER"  # GroupDeprecation
    assert args[0][1]["workspace_id"] == workspace.id
    assert args[0][1]["workspace_user"]["user_id"] == workspace_user_1.user_id
    assert args[0][1]["workspace_user"]["permissions"] == "MEMBER"


@pytest.mark.django_db(transaction=True)
@patch("baserow.ws.signals.broadcast_to_group")
@patch("baserow.ws.signals.broadcast_to_users")
@pytest.mark.websockets
def test_workspace_user_deleted(
    mock_broadcast_to_users, mock_broadcast_to_workspace, data_fixture
):
    user_1 = data_fixture.create_user()
    user_2 = data_fixture.create_user()
    workspace = data_fixture.create_workspace()
    workspace_user_1 = data_fixture.create_user_workspace(
        user=user_1, workspace=workspace
    )
    workspace_user_id = workspace_user_1.id
    data_fixture.create_user_workspace(user=user_2, workspace=workspace)
    CoreHandler().delete_workspace_user(user=user_2, workspace_user=workspace_user_1)

    mock_broadcast_to_users.delay.assert_called_once()
    args = mock_broadcast_to_users.delay.call_args
    assert args[0][0] == [user_1.id]
    assert args[0][1]["type"] == "group_user_deleted"
    assert args[0][1]["id"] == workspace_user_id
    assert args[0][1]["group_id"] == workspace.id  # GroupDeprecation
    assert (
        args[0][1]["group_user"]["user_id"] == workspace_user_1.user_id
    )  # GroupDeprecation
    assert args[0][1]["workspace_id"] == workspace.id
    assert args[0][1]["workspace_user"]["user_id"] == workspace_user_1.user_id

    mock_broadcast_to_workspace.delay.assert_called_once()
    args = mock_broadcast_to_workspace.delay.call_args
    assert args[0][0] == workspace.id
    assert args[0][1]["type"] == "group_user_deleted"
    assert args[0][1]["id"] == workspace_user_id
    assert args[0][1]["group_id"] == workspace.id  # GroupDeprecation
    assert (
        args[0][1]["group_user"]["user_id"] == workspace_user_1.user_id
    )  # GroupDeprecation
    assert args[0][1]["workspace_id"] == workspace.id
    assert args[0][1]["workspace_user"]["user_id"] == workspace_user_1.user_id


@pytest.mark.django_db(transaction=True)
@patch("baserow.ws.signals.broadcast_to_group")
@patch("baserow.ws.signals.broadcast_to_users")
@pytest.mark.websockets
def test_user_leaves_workspace(
    mock_broadcast_to_users, mock_broadcast_to_workspace, data_fixture
):
    user_1 = data_fixture.create_user()
    user_2 = data_fixture.create_user()
    workspace = data_fixture.create_workspace()
    workspace_user_1 = data_fixture.create_user_workspace(
        user=user_1, workspace=workspace
    )
    workspace_user_id = workspace_user_1.id
    data_fixture.create_user_workspace(user=user_2, workspace=workspace)
    CoreHandler().leave_workspace(user_1, workspace)

    mock_broadcast_to_users.delay.assert_called_once()
    args = mock_broadcast_to_users.delay.call_args
    assert args[0][0] == [user_1.id]
    assert args[0][1]["type"] == "group_user_deleted"
    assert args[0][1]["id"] == workspace_user_id
    assert args[0][1]["group_id"] == workspace.id  # GroupDeprecation
    assert (
        args[0][1]["group_user"]["user_id"] == workspace_user_1.user_id
    )  # GroupDeprecation
    assert args[0][1]["workspace_id"] == workspace.id
    assert args[0][1]["workspace_user"]["user_id"] == workspace_user_1.user_id

    mock_broadcast_to_workspace.delay.assert_called_once()
    args = mock_broadcast_to_workspace.delay.call_args
    assert args[0][0] == workspace.id
    assert args[0][1]["type"] == "group_user_deleted"
    assert args[0][1]["id"] == workspace_user_id
    assert args[0][1]["group_id"] == workspace.id  # GroupDeprecation
    assert (
        args[0][1]["group_user"]["user_id"] == workspace_user_1.user_id
    )  # GroupDeprecation
    assert args[0][1]["workspace_id"] == workspace.id
    assert args[0][1]["workspace_user"]["user_id"] == workspace_user_1.user_id


@pytest.mark.django_db(transaction=True)
@patch("baserow.ws.signals.broadcast_to_users")
@pytest.mark.websockets
def test_workspaces_reordered(mock_broadcast_to_users, data_fixture):
    user = data_fixture.create_user()
    workspace_1 = data_fixture.create_workspace(user=user)
    workspace_2 = data_fixture.create_workspace(user=user)
    workspace_3 = data_fixture.create_workspace(user=user)

    CoreHandler().order_workspaces(
        user=user, workspace_ids=[workspace_1.id, workspace_2.id, workspace_3.id]
    )

    mock_broadcast_to_users.delay.assert_called_once()
    args = mock_broadcast_to_users.delay.call_args
    assert args[0][0] == [user.id]
    assert args[0][1]["type"] == "groups_reordered"
    workspace_ids = [
        workspace_1.id,
        workspace_2.id,
        workspace_3.id,
    ]
    assert args[0][1]["group_ids"] == workspace_ids  # GroupDeprecation
    assert args[0][1]["workspace_ids"] == workspace_ids


@pytest.mark.django_db(transaction=True)
@patch("baserow.ws.signals.broadcast_application_created")
@pytest.mark.websockets
def test_application_created(mock_broadcast_application_created, data_fixture):
    user = data_fixture.create_user()
    workspace = data_fixture.create_workspace(user=user)
    websocket_id = "test"
    user.web_socket_id = websocket_id
    database = CoreHandler().create_application(
        user=user, workspace=workspace, type_name="database", name="Database"
    )

    mock_broadcast_application_created.delay.assert_called_once()
    args = mock_broadcast_application_created.delay.call_args
    assert args[0][0] == database.id
    assert args[0][1] == websocket_id


@pytest.mark.django_db(transaction=True)
@patch("baserow.ws.signals.broadcast_to_permitted_users")
@pytest.mark.websockets
def test_application_updated(mock_broadcast_to_permitted_users, data_fixture):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user)
    CoreHandler().update_application(user=user, application=database, name="Database")

    mock_broadcast_to_permitted_users.delay.assert_called_once()
    args = mock_broadcast_to_permitted_users.delay.call_args
    assert args[0][4]["type"] == "application_updated"
    assert args[0][4]["application_id"] == database.id
    assert args[0][4]["application"]["id"] == database.id


@pytest.mark.django_db(transaction=True)
@patch("baserow.ws.signals.broadcast_to_permitted_users")
@pytest.mark.websockets
def test_application_deleted(mock_broadcast_to_permitted_users, data_fixture):
    user = data_fixture.create_user()
    database = data_fixture.create_database_application(user=user)
    database_id = database.id
    CoreHandler().delete_application(user=user, application=database)

    mock_broadcast_to_permitted_users.delay.assert_called_once()
    args = mock_broadcast_to_permitted_users.delay.call_args
    assert args[0][4]["type"] == "application_deleted"
    assert args[0][4]["application_id"] == database_id


@pytest.mark.django_db(transaction=True)
@patch("baserow.ws.signals.broadcast_to_group")
@pytest.mark.websockets
def test_applications_reordered(mock_broadcast_to_channel_group, data_fixture):
    user = data_fixture.create_user()
    workspace = data_fixture.create_workspace(user=user)
    database = data_fixture.create_database_application(workspace=workspace)
    CoreHandler().order_applications(
        user=user, workspace=workspace, order=[database.id]
    )

    mock_broadcast_to_channel_group.delay.assert_called_once()
    args = mock_broadcast_to_channel_group.delay.call_args
    assert args[0][0] == database.workspace_id
    assert args[0][1]["type"] == "applications_reordered"
    assert args[0][1]["group_id"] == workspace.id  # GroupDeprecation
    assert args[0][1]["workspace_id"] == workspace.id
    assert args[0][1]["order"] == [generate_hash(database.id)]


@pytest.mark.django_db(transaction=True)
@patch("baserow.ws.signals.broadcast_application_created")
@pytest.mark.websockets
def test_duplicate_application(mock_broadcast_to_permitted_users, data_fixture):
    user = data_fixture.create_user()
    workspace = data_fixture.create_workspace(user=user)
    database = data_fixture.create_database_application(workspace=workspace)

    with transaction.atomic():
        application_clone = CoreHandler().duplicate_application(
            user=user, application=database
        )

    mock_broadcast_to_permitted_users.delay.assert_called_once()
    args = mock_broadcast_to_permitted_users.delay.call_args
    assert args[0][0] == application_clone.id
