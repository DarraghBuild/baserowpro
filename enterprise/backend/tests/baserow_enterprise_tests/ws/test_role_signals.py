from django.apps import apps
from django.db import transaction

import pytest
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator

from baserow.config.asgi import application
from baserow.core.apps import sync_operations_after_migrate
from baserow_enterprise.apps import sync_default_roles_after_migrate
from baserow_enterprise.role.constants import NO_ROLE_LOW_PRIORITY_ROLE_UID
from baserow_enterprise.role.handler import RoleAssignmentHandler
from baserow_enterprise.role.models import Role
from baserow_enterprise.teams.handler import TeamHandler
from tests.baserow.contrib.database.utils import received_message
from channels.layers import get_channel_layer
from baserow.ws.tasks import closing_group_send


# We have to run this every time between test executions since we are using
# `transaction=True`for some of the tests which flushes the DB and deletes the roles
@pytest.fixture(autouse=True)
def synced_roles(db):
    sync_operations_after_migrate(None, apps=apps)
    sync_default_roles_after_migrate(None, apps=apps)

    def resetRoleAssignmentHandlerCache():
        # Reset the cache at the beginning of the tests to prevent invalid cache when
        # a previous transaction has been rolled back.

        RoleAssignmentHandler._init = False

    transaction.on_commit(resetRoleAssignmentHandlerCache)

    yield

    sync_operations_after_migrate(None, apps=apps)
    sync_default_roles_after_migrate(None, apps=apps)
    transaction.on_commit(resetRoleAssignmentHandlerCache)


@pytest.fixture(autouse=True)
def enable_enterprise_for_all_tests_here(enable_enterprise):
    pass


@pytest.fixture(autouse=True)
def use_async_event_loop_here(async_event_loop):
    pass


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.websockets
async def test_unsubscribe_subject_from_table_role_deleted(data_fixture):
    user, token = data_fixture.create_user_and_token()
    workspace = data_fixture.create_workspace(members=[user])
    database = data_fixture.create_database_application(workspace=workspace)
    table = data_fixture.create_database_table(database=database)
    builder_role = Role.objects.get(uid="BUILDER")

    # Assign an initial role to the user
    await sync_to_async(RoleAssignmentHandler().assign_role)(
        user, workspace, builder_role
    )

    # Establish websocket connection and subscribe to table
    communicator = WebsocketCommunicator(
        application,
        f"ws/core/?jwt_token={token}",
        headers=[(b"origin", b"http://localhost")],
    )
    await communicator.connect()
    await communicator.receive_json_from()

    await communicator.send_json_to({"page": "table", "table_id": table.id})
    await communicator.receive_json_from()

    # Remove role from user
    await sync_to_async(RoleAssignmentHandler().assign_role)(user, workspace, None)

    # Make sure the user has been un-subscribed
    assert await received_message(communicator, "page_discard") is True
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.websockets
async def test_unsubscribe_subject_from_table_role_no_role(data_fixture):
    user, token = data_fixture.create_user_and_token()
    workspace = data_fixture.create_workspace(members=[user])
    database = data_fixture.create_database_application(workspace=workspace)
    table = data_fixture.create_database_table(database=database)
    builder_role = Role.objects.get(uid="BUILDER")
    no_role_role = Role.objects.get(uid=NO_ROLE_LOW_PRIORITY_ROLE_UID)

    # Assign an initial role to the user
    await sync_to_async(RoleAssignmentHandler().assign_role)(
        user, workspace, builder_role
    )

    # Establish websocket connection and subscribe to table
    communicator = WebsocketCommunicator(
        application,
        f"ws/core/?jwt_token={token}",
        headers=[(b"origin", b"http://localhost")],
    )
    await communicator.connect()
    await communicator.receive_json_from()

    await communicator.send_json_to({"page": "table", "table_id": table.id})
    await communicator.receive_json_from()

    # Remove role from user
    await sync_to_async(RoleAssignmentHandler().assign_role)(
        user, workspace, no_role_role
    )

    # Make sure the user has been un-subscribed
    assert await received_message(communicator, "page_discard") is True
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.websockets
async def test_unsubscribe_subject_from_table_unrelated_user(data_fixture):
    user = data_fixture.create_user()
    unrelated_user, token = data_fixture.create_user_and_token()
    workspace = data_fixture.create_workspace(members=[user, unrelated_user])
    database = data_fixture.create_database_application(workspace=workspace)
    table = data_fixture.create_database_table(database=database)
    builder_role = Role.objects.get(uid="BUILDER")

    # Assign an initial role to the user
    await sync_to_async(RoleAssignmentHandler().assign_role)(
        user, workspace, builder_role
    )

    # Establish websocket connection and subscribe to table
    communicator = WebsocketCommunicator(
        application,
        f"ws/core/?jwt_token={token}",
        headers=[(b"origin", b"http://localhost")],
    )
    await communicator.connect()
    await communicator.receive_json_from()

    await communicator.send_json_to({"page": "table", "table_id": table.id})
    await communicator.receive_json_from()

    # Remove role from user
    await sync_to_async(RoleAssignmentHandler().assign_role)(user, workspace, None)

    # Make sure the user has been un-subscribed
    assert await received_message(communicator, "page_discard") is False
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.websockets
async def test_unsubscribe_subject_from_table_new_role_no_access(data_fixture):
    user, token = data_fixture.create_user_and_token()
    workspace = data_fixture.create_workspace(members=[user])
    database = data_fixture.create_database_application(workspace=workspace)
    table = data_fixture.create_database_table(database=database)
    no_access_role = Role.objects.get(uid="NO_ACCESS")

    # Establish websocket connection and subscribe to table
    communicator = WebsocketCommunicator(
        application,
        f"ws/core/?jwt_token={token}",
        headers=[(b"origin", b"http://localhost")],
    )
    await communicator.connect()
    await communicator.receive_json_from()

    await communicator.send_json_to({"page": "table", "table_id": table.id})
    await communicator.receive_json_from()

    # Deny user access to the table
    await sync_to_async(RoleAssignmentHandler().assign_role)(
        user, workspace, no_access_role, table
    )

    # Make sure the user has been un-subscribed
    assert await received_message(communicator, "page_discard") is True
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.websockets
async def test_unsubscribe_subject_from_table_role_updated(data_fixture):
    user, token = data_fixture.create_user_and_token()
    workspace = data_fixture.create_workspace(members=[user])
    database = data_fixture.create_database_application(workspace=workspace)
    table = data_fixture.create_database_table(database=database)
    builder_role = Role.objects.get(uid="BUILDER")
    no_access_role = Role.objects.get(uid="NO_ACCESS")

    # Assign an initial role to the user
    await sync_to_async(RoleAssignmentHandler().assign_role)(
        user, workspace, builder_role
    )

    # Establish websocket connection and subscribe to table
    communicator = WebsocketCommunicator(
        application,
        f"ws/core/?jwt_token={token}",
        headers=[(b"origin", b"http://localhost")],
    )
    await communicator.connect()
    await communicator.receive_json_from()

    await communicator.send_json_to({"page": "table", "table_id": table.id})
    await communicator.receive_json_from()

    # Remove role from user
    await sync_to_async(RoleAssignmentHandler().assign_role)(
        user, workspace, no_access_role
    )

    # Make sure the user has been un-subscribed
    assert await received_message(communicator, "page_discard") is True
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.websockets
async def test_unsubscribe_subject_from_table_should_still_have_access(data_fixture):
    user, token = data_fixture.create_user_and_token()
    workspace = data_fixture.create_workspace(user=user)
    database = data_fixture.create_database_application(workspace=workspace)
    table = data_fixture.create_database_table(database=database)
    builder_role = Role.objects.get(uid="BUILDER")

    # Assign an initial role to the user
    await sync_to_async(RoleAssignmentHandler().assign_role)(
        user, workspace, builder_role, table
    )

    # Establish websocket connection and subscribe to table
    communicator = WebsocketCommunicator(
        application,
        f"ws/core/?jwt_token={token}",
        headers=[(b"origin", b"http://localhost")],
    )
    await communicator.connect()
    await communicator.receive_json_from()

    await communicator.send_json_to({"page": "table", "table_id": table.id})
    await communicator.receive_json_from()

    # Remove role from user, in this case the user still has their workspace level
    # role and is therefore still able to see the table
    await sync_to_async(RoleAssignmentHandler().assign_role)(
        user, workspace, None, table
    )

    # Make sure the user is still subscribed
    assert await received_message(communicator, "page_discard") is False
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.websockets
async def test_unsubscribe_subject_from_table_teams(
    data_fixture, enterprise_data_fixture
):
    user, token = data_fixture.create_user_and_token()
    workspace = data_fixture.create_workspace(custom_permissions=[(user, "NO_ACCESS")])
    team = enterprise_data_fixture.create_team(workspace=workspace)
    database = data_fixture.create_database_application(workspace=workspace)
    table = data_fixture.create_database_table(database=database)
    builder_role = Role.objects.get(uid="BUILDER")

    # Add user to team
    enterprise_data_fixture.create_subject(team, user)

    # Set initial role for team
    await sync_to_async(RoleAssignmentHandler().assign_role)(
        team, workspace, builder_role, table
    )

    # Establish websocket connection and subscribe to table
    communicator = WebsocketCommunicator(
        application,
        f"ws/core/?jwt_token={token}",
        headers=[(b"origin", b"http://localhost")],
    )
    await communicator.connect()
    await communicator.receive_json_from()

    await communicator.send_json_to({"page": "table", "table_id": table.id})
    await communicator.receive_json_from()

    await sync_to_async(RoleAssignmentHandler().assign_role)(
        team, workspace, None, table
    )

    assert await received_message(communicator, "page_discard") is True
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.websockets
async def test_unsubscribe_subject_from_table_teams_when_team_trashed(
    data_fixture, enterprise_data_fixture
):
    user, token = data_fixture.create_user_and_token()
    workspace = data_fixture.create_workspace(custom_permissions=[(user, "NO_ACCESS")])
    team = enterprise_data_fixture.create_team(workspace=workspace)
    database = data_fixture.create_database_application(workspace=workspace)
    table = data_fixture.create_database_table(database=database)
    builder_role = Role.objects.get(uid="BUILDER")

    # Add user to team
    enterprise_data_fixture.create_subject(team, user)

    # Set initial role for team
    await sync_to_async(RoleAssignmentHandler().assign_role)(
        team, workspace, builder_role, table
    )

    # Establish websocket connection and subscribe to table
    communicator = WebsocketCommunicator(
        application,
        f"ws/core/?jwt_token={token}",
        headers=[(b"origin", b"http://localhost")],
    )
    await communicator.connect()
    await communicator.receive_json_from()

    await communicator.send_json_to({"page": "table", "table_id": table.id})
    await communicator.receive_json_from()

    await sync_to_async(TeamHandler().delete_team)(user, team)

    assert await received_message(communicator, "page_discard") is True
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.websockets
async def test_unsubscribe_subject_from_table_teams_still_connected(
    data_fixture, enterprise_data_fixture
):
    user, token = data_fixture.create_user_and_token()
    workspace = data_fixture.create_workspace(user=user)
    team = enterprise_data_fixture.create_team(workspace=workspace)
    database = data_fixture.create_database_application(workspace=workspace)
    table = data_fixture.create_database_table(database=database)
    builder_role = Role.objects.get(uid="BUILDER")

    # Add user to team
    enterprise_data_fixture.create_subject(team, user)

    # Set initial role for team
    await sync_to_async(RoleAssignmentHandler().assign_role)(
        team, workspace, builder_role, table
    )

    # Establish websocket connection and subscribe to table
    communicator = WebsocketCommunicator(
        application,
        f"ws/core/?jwt_token={token}",
        headers=[(b"origin", b"http://localhost")],
    )
    await communicator.connect()
    await communicator.receive_json_from()

    await communicator.send_json_to({"page": "table", "table_id": table.id})
    await communicator.receive_json_from()

    await sync_to_async(RoleAssignmentHandler().assign_role)(
        team, workspace, None, table
    )

    assert await received_message(communicator, "page_discard") is False
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.websockets
async def test_unsubscribe_subject_from_table_teams_multiple_users(
    data_fixture, enterprise_data_fixture
):
    user, token = data_fixture.create_user_and_token()
    user_2, token_2 = data_fixture.create_user_and_token()
    workspace = data_fixture.create_workspace(
        custom_permissions=[(user, "NO_ACCESS"), (user_2, "NO_ACCESS")]
    )
    team = enterprise_data_fixture.create_team(workspace=workspace)
    database = data_fixture.create_database_application(workspace=workspace)
    table = data_fixture.create_database_table(database=database)
    builder_role = Role.objects.get(uid="BUILDER")

    # Add user to team
    enterprise_data_fixture.create_subject(team, user)
    enterprise_data_fixture.create_subject(team, user_2)

    # Set initial role for team
    await sync_to_async(RoleAssignmentHandler().assign_role)(
        team, workspace, builder_role, table
    )

    # Establish websocket connection and subscribe to table
    communicator = WebsocketCommunicator(
        application,
        f"ws/core/?jwt_token={token}",
        headers=[(b"origin", b"http://localhost")],
    )
    await communicator.connect()
    await communicator.receive_json_from()

    await communicator.send_json_to({"page": "table", "table_id": table.id})
    await communicator.receive_json_from()

    communicator_2 = WebsocketCommunicator(
        application,
        f"ws/core/?jwt_token={token_2}",
        headers=[(b"origin", b"http://localhost")],
    )
    await communicator_2.connect()
    await communicator_2.receive_json_from()

    await communicator_2.send_json_to({"page": "table", "table_id": table.id})
    await communicator_2.receive_json_from()

    await sync_to_async(RoleAssignmentHandler().assign_role)(
        team, workspace, None, table
    )

    assert await received_message(communicator, "page_discard") is True
    assert await received_message(communicator_2, "page_discard") is True
    await communicator.disconnect()
    await communicator_2.disconnect()


# @pytest.mark.asyncio
# @pytest.mark.django_db(transaction=True)
# @pytest.mark.websockets
# async def test_unsubscribe_user_from_tables_and_rows_when_removed_from_workspace(data_fixture):
#     channel_layer = get_channel_layer()
#     user_1, token_1 = data_fixture.create_user_and_token()
#     workspace_1 = data_fixture.create_workspace(user=user_1)
#     workspace_2 = data_fixture.create_workspace(user=user_1)
#     application_1 = data_fixture.create_database_application(
#         workspace=workspace_1, order=1
#     )
#     application_2 = data_fixture.create_database_application(
#         workspace=workspace_2, order=1
#     )
#     table_1 = data_fixture.create_database_table(database=application_1)
#     table_1_model = table_1.get_model()
#     row_1 = table_1_model.objects.create()
#     table_2 = data_fixture.create_database_table(database=application_2)

#     communicator = WebsocketCommunicator(
#         application,
#         f"ws/core/?jwt_token={token_1}",
#         headers=[(b"origin", b"http://localhost")],
#     )
#     await communicator.connect()
#     response = await communicator.receive_json_from(timeout=0.1)

#     # Subscribe user to a table and a row from workspace 1
#     await communicator.send_json_to({"page": "table", "table_id": table_1.id})
#     response = await communicator.receive_json_from(timeout=0.1)

#     await communicator.send_json_to(
#         {"page": "row", "table_id": table_1.id, "row_id": row_1.id}
#     )
#     response = await communicator.receive_json_from(timeout=0.1)

#     # Subscribe user to a table from workspace 2
#     await communicator.send_json_to({"page": "table", "table_id": table_2.id})
#     response = await communicator.receive_json_from(timeout=0.1)

#     # Send a message to consumers that user was removed from the workspace 1
#     await sync_to_async(unsubscribe_user_from_tables_when_removed_from_workspace)(
#         user_1.id, workspace_1.id
#     )

#     # Receiving messages about being removed from the pages
#     response = await communicator.receive_json_from(timeout=0.1)
#     assert response == {
#         "page": "table",
#         "parameters": {
#             "table_id": table_1.id,
#         },
#         "type": "page_discard",
#     }

#     response = await communicator.receive_json_from(timeout=0.1)
#     assert response == {
#         "page": "row",
#         "parameters": {
#             "table_id": table_1.id,
#             "row_id": row_1.id,
#         },
#         "type": "page_discard",
#     }

#     # User should not receive any messages to a table in workspace 1
#     await closing_group_send(channel_layer, f"table-{table_1.id}", {"test": "message"})
#     await communicator.receive_nothing(timeout=0.1)

#     # User should not receive any messages to a row in workspace 1
#     await closing_group_send(
#         channel_layer, f"table-{table_1.id}-row-{row_1.id}", {"test": "message"}
#     )
#     await communicator.receive_nothing(timeout=0.1)

#     # User should still receive messages to a table in workspace 2
#     await closing_group_send(
#         channel_layer,
#         f"table-{table_2.id}",
#         {
#             "type": "broadcast_to_group",
#             "payload": {"test": "message"},
#             "ignore_web_socket_id": None,
#         },
#     )
#     response = await communicator.receive_json_from(timeout=0.1)
#     assert response == {"test": "message"}

#     assert communicator.output_queue.qsize() == 0
#     await communicator.disconnect()