from operator import is_
import pytest
from django.shortcuts import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from baserow.contrib.database.fields.handler import FieldHandler
from baserow.contrib.database.rows.handler import RowHandler

from baserow.test_utils.helpers import is_dict_subset


@pytest.mark.field_collaborator
@pytest.mark.django_db
def test_collaborator_field_type_create(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token(
        email="test@test.nl", password="password", first_name="Test1"
    )
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table = data_fixture.create_database_table(name="Example", database=database)

    response = api_client.post(
        reverse("api:database:fields:list", kwargs={"table_id": table.id}),
        {
            "name": "Collaborator 1",
            "type": "collaborator",
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    field_1_id = response_json["id"]
    assert response_json["name"] == "Collaborator 1"
    assert response_json["type"] == "collaborator"


@pytest.mark.field_collaborator
@pytest.mark.django_db
def test_collaborator_field_type_update(api_client, data_fixture):
    group = data_fixture.create_group()
    user, token = data_fixture.create_user_and_token(
        email="test@test.nl", password="password", first_name="Test1", group=group
    )
    database = data_fixture.create_database_application(
        user=user, name="Placeholder", group=group
    )
    table = data_fixture.create_database_table(name="Example", database=database)
    field_handler = FieldHandler()
    collaborator_field = field_handler.create_field(
        user=user,
        table=table,
        type_name="collaborator",
        name="Collaborator 1",
    )

    response = api_client.patch(
        reverse("api:database:fields:item", kwargs={"field_id": collaborator_field.id}),
        {"name": "New collaborator 1"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["name"] == "New collaborator 1"
    assert response_json["type"] == "collaborator"


@pytest.mark.field_collaborator
@pytest.mark.django_db
def test_collaborator_field_type_delete(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token(
        email="test@test.nl", password="password", first_name="Test1"
    )
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table = data_fixture.create_database_table(name="Example", database=database)
    field_handler = FieldHandler()
    collaborator_field = field_handler.create_field(
        user=user,
        table=table,
        type_name="collaborator",
        name="Collaborator 1",
    )

    response = api_client.delete(
        reverse("api:database:fields:item", kwargs={"field_id": collaborator_field.id}),
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_200_OK
    collaborator_field.refresh_from_db()
    assert collaborator_field.trashed is True


@pytest.mark.field_collaborator
@pytest.mark.api_rows
@pytest.mark.django_db
def test_collaborator_field_type_insert_row_validation(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token(
        email="test@test.nl", password="password", first_name="Test1"
    )
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table = data_fixture.create_database_table(name="Example", database=database)
    field_handler = FieldHandler()
    collaborator_field = field_handler.create_field(
        user=user,
        table=table,
        type_name="collaborator",
        name="Collaborator 1",
    )

    # not a list

    response = api_client.post(
        reverse("api:database:rows:list", kwargs={"table_id": table.id}),
        {f"field_{collaborator_field.id}": "Nothing"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_REQUEST_BODY_VALIDATION"
    assert (
        response_json["detail"][f"field_{collaborator_field.id}"]["non_field_errors"][
            0
        ]["code"]
        == "not_a_list"
    )

    # wrong user id

    response = api_client.post(
        reverse("api:database:rows:list", kwargs={"table_id": table.id}),
        {f"field_{collaborator_field.id}": [{"id": 999999}]},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_REQUEST_BODY_VALIDATION"
    assert (
        response_json["detail"]
        == "The provided user id [999999] is not a valid collaborator."
    )


@pytest.mark.field_collaborator
@pytest.mark.api_rows
@pytest.mark.django_db
def test_collaborator_field_type_insert_row(api_client, data_fixture):
    group = data_fixture.create_group()
    user, token = data_fixture.create_user_and_token(
        email="test@test.nl", password="password", first_name="Test1", group=group
    )
    user2 = data_fixture.create_user(group=group)
    user3 = data_fixture.create_user(group=group)
    database = data_fixture.create_database_application(
        user=user, group=group, name="Placeholder"
    )
    table = data_fixture.create_database_table(name="Example", database=database)
    field_handler = FieldHandler()
    collaborator_field = field_handler.create_field(
        user=user,
        table=table,
        type_name="collaborator",
        name="Collaborator 1",
    )

    # empty list

    response = api_client.post(
        reverse("api:database:rows:list", kwargs={"table_id": table.id}),
        {f"field_{collaborator_field.id}": []},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_200_OK
    assert is_dict_subset({f"field_{collaborator_field.id}": []}, response.json())

    # list

    response = api_client.post(
        reverse("api:database:rows:list", kwargs={"table_id": table.id}),
        {f"field_{collaborator_field.id}": [{"id": user2.id}, {"id": user3.id}]},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_200_OK
    assert is_dict_subset(
        {
            f"field_{collaborator_field.id}": [
                {"id": user2.id, "name": user2.first_name},
                {"id": user3.id, "name": user3.first_name},
            ]
        },
        response.json(),
    )


@pytest.mark.field_collaborator
@pytest.mark.api_rows
@pytest.mark.django_db
def test_collaborator_field_type_update_row_validation(api_client, data_fixture):
    group = data_fixture.create_group()
    user, token = data_fixture.create_user_and_token(
        email="test@test.nl", password="password", first_name="Test1", group=group
    )
    database = data_fixture.create_database_application(
        user=user, group=group, name="Placeholder"
    )
    table = data_fixture.create_database_table(name="Example", database=database)
    field_handler = FieldHandler()
    collaborator_field = field_handler.create_field(
        user=user,
        table=table,
        type_name="collaborator",
        name="Collaborator 1",
    )
    row_handler = RowHandler()
    row = row_handler.create_row(
        user=user, table=table, values={collaborator_field.id: [{"id": user.id}]}
    )

    # not a list

    response = api_client.patch(
        reverse(
            "api:database:rows:item", kwargs={"table_id": table.id, "row_id": row.id}
        ),
        {f"field_{collaborator_field.id}": 43},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_REQUEST_BODY_VALIDATION"
    assert (
        response_json["detail"][f"field_{collaborator_field.id}"]["non_field_errors"][
            0
        ]["code"]
        == "not_a_list"
    )

    # wrong user id

    response = api_client.patch(
        reverse(
            "api:database:rows:item", kwargs={"table_id": table.id, "row_id": row.id}
        ),
        {f"field_{collaborator_field.id}": [{"id": 999999}]},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    response_json = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response_json["error"] == "ERROR_REQUEST_BODY_VALIDATION"
    assert (
        response_json["detail"]
        == "The provided user id [999999] is not a valid collaborator."
    )


@pytest.mark.field_collaborator
@pytest.mark.api_rows
@pytest.mark.django_db
def test_collaborator_field_type_update_row(api_client, data_fixture):
    group = data_fixture.create_group()
    user, token = data_fixture.create_user_and_token(
        email="test@test.nl", password="password", first_name="Test1", group=group
    )
    user2 = data_fixture.create_user(group=group)
    user3 = data_fixture.create_user(group=group)
    database = data_fixture.create_database_application(
        user=user, group=group, name="Placeholder"
    )
    table = data_fixture.create_database_table(name="Example", database=database)
    field_handler = FieldHandler()
    collaborator_field = field_handler.create_field(
        user=user,
        table=table,
        type_name="collaborator",
        name="Collaborator 1",
    )
    row_handler = RowHandler()
    row = row_handler.create_row(
        user=user, table=table, values={collaborator_field.id: [{"id": user.id}]}
    )

    # list

    response = api_client.patch(
        reverse(
            "api:database:rows:item", kwargs={"table_id": table.id, "row_id": row.id}
        ),
        {f"field_{collaborator_field.id}": [{"id": user2.id}, {"id": user3.id}]},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_200_OK
    response_json = response.json()
    assert response_json[f"field_{collaborator_field.id}"][0]["id"] == user2.id
    assert response_json[f"field_{collaborator_field.id}"][1]["id"] == user3.id

    # empty list

    response = api_client.patch(
        reverse(
            "api:database:rows:item", kwargs={"table_id": table.id, "row_id": row.id}
        ),
        {f"field_{collaborator_field.id}": []},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_200_OK
    assert is_dict_subset({f"field_{collaborator_field.id}": []}, response.json())


@pytest.mark.field_collaborator
@pytest.mark.api_rows
@pytest.mark.django_db
def test_collaborator_field_type_delete_row(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token(
        email="test@test.nl", password="password", first_name="Test1"
    )
    database = data_fixture.create_database_application(user=user, name="Placeholder")
    table = data_fixture.create_database_table(name="Example", database=database)
    field_handler = FieldHandler()
    collaborator_field = field_handler.create_field(
        user=user,
        table=table,
        type_name="collaborator",
        name="Collaborator 1",
    )
    row_handler = RowHandler()
    row = row_handler.create_row(
        user=user, table=table, values={collaborator_field.id: [{"id": user.id}]}
    )

    response = api_client.delete(
        reverse(
            "api:database:rows:item", kwargs={"table_id": table.id, "row_id": row.id}
        ),
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_204_NO_CONTENT
    model = table.get_model()
    assert model.objects.count() == 0


# TODO: batch insert rows + validation
# TODO: batch update rows + validation
# TODO: batch delete rows
