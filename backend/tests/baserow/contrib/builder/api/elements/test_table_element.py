from django.urls import reverse

import pytest
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_can_get_a_table_element(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    table_element = data_fixture.create_builder_table_element(user=user)

    url = reverse("api:builder:element:list", kwargs={"page_id": table_element.page.id})
    response = api_client.get(
        url,
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    [column_element_returned] = response.json()
    assert response.status_code == HTTP_200_OK
    assert column_element_returned["id"] == table_element.id
    assert column_element_returned["type"] == "table"


@pytest.mark.django_db
def test_can_create_a_table_element(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)

    url = reverse("api:builder:element:list", kwargs={"page_id": page.id})

    response = api_client.post(
        url,
        {
            "type": "table",
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_200_OK
    assert response.json()["type"] == "table"
    assert [
        {key: value for key, value in f.items() if key != "id"}
        for f in response.json()["fields"]
    ] == [
        {"name": "Column 1", "type": "text", "value": ""},
        {"name": "Column 2", "type": "text", "value": ""},
        {"name": "Column 3", "type": "text", "value": ""},
    ]


@pytest.mark.django_db
def test_can_update_a_table_element_fields(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    table_element = data_fixture.create_builder_table_element(user=user)

    url = reverse("api:builder:element:item", kwargs={"element_id": table_element.id})

    response = api_client.patch(
        url,
        {
            "fields": [
                {"name": "Name", "type": "text", "value": "get('test1')"},
                {
                    "name": "Color",
                    "type": "link",
                    "url": "get('test2')",
                    "link_name": "get('test3')",
                },
                {"name": "Question", "type": "text", "value": "get('test3')"},
            ],
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_200_OK
    assert [
        {key: value for key, value in f.items() if key != "id"}
        for f in response.json()["fields"]
    ] == [
        {"name": "Name", "type": "text", "value": "get('test1')"},
        {
            "name": "Color",
            "type": "link",
            "url": "get('test2')",
            "link_name": "get('test3')",
        },
        {"name": "Question", "type": "text", "value": "get('test3')"},
    ]


@pytest.mark.django_db
def test_cant_update_a_table_element_fields_with_wrong_field_type(
    api_client, data_fixture
):
    user, token = data_fixture.create_user_and_token()
    table_element = data_fixture.create_builder_table_element(user=user)

    url = reverse("api:builder:element:item", kwargs={"element_id": table_element.id})

    response = api_client.patch(
        url,
        {
            "fields": [
                {"name": "Name", "type": "missing", "value": "get('test1')"},
            ],
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["detail"]["fields"][0][0]["code"] == "INVALID_FIELD_TYPE"


@pytest.mark.django_db
def test_cant_update_a_table_element_fields_with_wrong_field_property(
    api_client, data_fixture
):
    user, token = data_fixture.create_user_and_token()
    table_element = data_fixture.create_builder_table_element(user=user)

    url = reverse("api:builder:element:item", kwargs={"element_id": table_element.id})

    response = api_client.patch(
        url,
        {
            "fields": [
                {"name": "Name", "type": "text", "missing": "get('test1')"},
            ],
        },
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["detail"]["fields"][0][0]["code"] == "INVALID_FIELD_PROPERTY"
