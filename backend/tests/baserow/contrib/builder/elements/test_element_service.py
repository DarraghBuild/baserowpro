from unittest.mock import patch

import pytest

from baserow.contrib.builder.elements.exceptions import (
    ElementDoesNotExist,
    ElementNotInPage,
)
from baserow.contrib.builder.elements.registries import element_type_registry
from baserow.contrib.builder.elements.service import ElementService
from baserow.core.exceptions import PermissionException


@pytest.mark.django_db
@patch("baserow.contrib.builder.elements.service.element_created")
def test_create_element(element_created_mock, data_fixture, stub_check_permissions):
    user = data_fixture.create_user()
    page = data_fixture.create_builder_page(user=user)

    for element_type in element_type_registry.get_all():
        sample_params = element_type.get_sample_params()

        element = ElementService().create_element(
            user, element_type, page=page, **sample_params
        )

        assert element_created_mock.called_with(element=element, user=user)


@pytest.mark.django_db
def test_create_element_permission_denied(data_fixture, stub_check_permissions):
    user = data_fixture.create_user()
    page = data_fixture.create_builder_page(user=user)

    element_type = element_type_registry.get("heading")

    with stub_check_permissions(raise_permission_denied=True), pytest.raises(
        PermissionException
    ):
        ElementService().create_element(
            user, element_type, page=page, **element_type.get_sample_params()
        )


@pytest.mark.django_db
def test_get_element(data_fixture):
    user = data_fixture.create_user()
    element = data_fixture.create_builder_header_element(user=user)

    assert ElementService().get_element(user, element.id).id == element.id


@pytest.mark.django_db
def test_get_element_does_not_exist(data_fixture):
    user = data_fixture.create_user()

    with pytest.raises(ElementDoesNotExist):
        assert ElementService().get_element(user, 0)


@pytest.mark.django_db
def test_get_element_permission_denied(data_fixture, stub_check_permissions):
    user = data_fixture.create_user()
    element = data_fixture.create_builder_header_element(user=user)

    with stub_check_permissions(raise_permission_denied=True), pytest.raises(
        PermissionException
    ):
        ElementService().get_element(user, element.id)


@pytest.mark.django_db
def test_get_elements(data_fixture, stub_check_permissions):
    user = data_fixture.create_user()
    page = data_fixture.create_builder_page(user=user)
    element1 = data_fixture.create_builder_header_element(page=page)
    element2 = data_fixture.create_builder_header_element(page=page)
    element3 = data_fixture.create_builder_paragraph_element(page=page)

    assert [p.id for p in ElementService().get_elements(user, page)] == [
        element1.id,
        element2.id,
        element3.id,
    ]

    def exclude_element_1(
        actor,
        operation_name,
        queryset,
        group=None,
        context=None,
        allow_if_template=False,
    ):
        return queryset.exclude(id=element1.id)

    with stub_check_permissions() as stub:
        stub.filter_queryset = exclude_element_1

        assert [p.id for p in ElementService().get_elements(user, page)] == [
            element2.id,
            element3.id,
        ]


@pytest.mark.django_db
@patch("baserow.contrib.builder.elements.service.element_deleted")
def test_delete_element(element_deleted_mock, data_fixture):
    user = data_fixture.create_user()
    element = data_fixture.create_builder_header_element(user=user)

    ElementService().delete_element(user, element)

    assert element_deleted_mock.called_with(element_id=element.id, user=user)


@pytest.mark.django_db(transaction=True)
def test_delete_element_permission_denied(data_fixture, stub_check_permissions):
    user = data_fixture.create_user()
    element = data_fixture.create_builder_header_element(user=user)

    with stub_check_permissions(raise_permission_denied=True), pytest.raises(
        PermissionException
    ):
        ElementService().delete_element(user, element)


@pytest.mark.django_db
@patch("baserow.contrib.builder.elements.service.element_updated")
def test_update_element(element_updated_mock, data_fixture):
    user = data_fixture.create_user()
    element = data_fixture.create_builder_header_element(user=user)

    element_updated = ElementService().update_element(
        user, element, {"config": {"value": "newValue"}}
    )

    assert element_updated_mock.called_with(element=element_updated, user=user)


@pytest.mark.django_db(transaction=True)
def test_update_element_permission_denied(data_fixture, stub_check_permissions):
    user = data_fixture.create_user()
    element = data_fixture.create_builder_header_element(user=user)

    with stub_check_permissions(raise_permission_denied=True), pytest.raises(
        PermissionException
    ):
        ElementService().update_element(
            user, element, {"config": {"value": "newValue"}}
        )


@pytest.mark.django_db
@patch("baserow.contrib.builder.elements.service.elements_reordered")
def test_order_elements(element_updated_mock, data_fixture):
    user = data_fixture.create_user()
    page = data_fixture.create_builder_page(user=user)
    element1 = data_fixture.create_builder_header_element(page=page)
    element2 = data_fixture.create_builder_header_element(page=page)
    element3 = data_fixture.create_builder_header_element(page=page)

    ElementService().order_elements(user, page, [element3.id, element1.id])

    assert element_updated_mock.called_with(
        full_order=[element2.id, element3.id, element1.id], page=page, user=user
    )


@pytest.mark.django_db
def test_order_elements_permission_denied(data_fixture, stub_check_permissions):
    user = data_fixture.create_user()
    page = data_fixture.create_builder_page(user=user)
    element1 = data_fixture.create_builder_header_element(page=page)
    element2 = data_fixture.create_builder_header_element(page=page)
    element3 = data_fixture.create_builder_header_element(page=page)

    with stub_check_permissions(raise_permission_denied=True), pytest.raises(
        PermissionException
    ):
        ElementService().order_elements(user, page, [element3.id, element1.id])


@pytest.mark.django_db
def test_order_elements_not_in_page(data_fixture, stub_check_permissions):
    user = data_fixture.create_user()
    page = data_fixture.create_builder_page(user=user)
    element1 = data_fixture.create_builder_header_element(page=page)
    element2 = data_fixture.create_builder_header_element(page=page)
    element3 = data_fixture.create_builder_header_element(user=user)

    with pytest.raises(ElementNotInPage):
        ElementService().order_elements(user, page, [element3.id, element1.id])

    def filter_queryset(
        actor,
        operation_name,
        queryset,
        group=None,
        context=None,
        allow_if_template=False,
    ):
        return queryset.exclude(id=element1.id)

    with stub_check_permissions() as stub, pytest.raises(ElementNotInPage):
        stub.filter_queryset = filter_queryset
        ElementService().order_elements(user, page, [element3.id, element1.id])
