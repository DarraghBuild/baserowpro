from unittest.mock import AsyncMock

import pytest
from channels.testing import WebsocketCommunicator

from baserow.config.asgi import application
from baserow.ws.auth import ANONYMOUS_USER_TOKEN
from baserow.ws.consumers import CoreConsumer, PageContext, PageScope, SubscribedPages
from baserow.ws.registries import PageType, page_registry


class AcceptingTestPageType(PageType):
    type = "test_page_type"
    parameters = ["test_param"]

    def can_add(self, user, web_socket_id, test_param, **kwargs):
        return True

    def get_group_name(self, test_param, **kwargs):
        return f"test-page-{test_param}"


class NotAcceptingTestPageType(AcceptingTestPageType):
    type = "test_page_type_not_accepting"

    def can_add(self, user, web_socket_id, test_param, **kwargs):
        return False


@pytest.fixture
def test_page_types():
    page_types = AcceptingTestPageType(), NotAcceptingTestPageType()
    page_registry.register(page_types[0])
    page_registry.register(page_types[1])
    yield page_types
    page_registry.unregister(AcceptingTestPageType.type)
    page_registry.unregister(NotAcceptingTestPageType.type)


# Core consumer


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.websockets
async def test_core_consumer_connect_not_authenticated(data_fixture):
    communicator = WebsocketCommunicator(
        application,
        f"ws/core/?jwt_token=",
        headers=[(b"origin", b"http://localhost")],
    )
    connected, subprotocol = await communicator.connect()
    assert connected is True

    response = await communicator.receive_json_from()
    assert response["type"] == "authentication"
    assert response["success"] is False
    assert response["web_socket_id"] is None
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.websockets
async def test_core_consumer_connect_authenticated(data_fixture):
    user_1, token_1 = data_fixture.create_user_and_token()
    communicator = WebsocketCommunicator(
        application,
        f"ws/core/?jwt_token={token_1}",
        headers=[(b"origin", b"http://localhost")],
    )
    connected, subprotocol = await communicator.connect()
    assert connected is True

    response = await communicator.receive_json_from()
    assert response["type"] == "authentication"
    assert response["success"] is True
    assert response["web_socket_id"] is not None
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.websockets
async def test_core_consumer_connect_authenticated_anonymous(data_fixture):
    user_1, token_1 = data_fixture.create_user_and_token()
    communicator = WebsocketCommunicator(
        application,
        f"ws/core/?jwt_token={ANONYMOUS_USER_TOKEN}",
        headers=[(b"origin", b"http://localhost")],
    )
    connected, subprotocol = await communicator.connect()
    assert connected is True

    response = await communicator.receive_json_from()
    assert response["type"] == "authentication"
    assert response["success"] is True
    assert response["web_socket_id"] is not None
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.websockets
async def test_core_consumer_add_to_page_success(data_fixture, test_page_types):
    user_1, token_1 = data_fixture.create_user_and_token()
    communicator = WebsocketCommunicator(
        application,
        f"ws/core/?jwt_token={token_1}",
        headers=[(b"origin", b"http://localhost")],
    )
    await communicator.connect()
    await communicator.receive_json_from()

    await communicator.send_json_to({"page": "test_page_type", "test_param": 1})
    response = await communicator.receive_json_from(timeout=0.1)
    assert response["type"] == "page_add"
    assert response["page"] == "test_page_type"
    assert response["parameters"]["test_param"] == 1

    # Adding again will have the same behavior
    # but the page will still be subscribed only once
    await communicator.send_json_to({"page": "test_page_type", "test_param": 1})
    response = await communicator.receive_json_from(timeout=0.1)
    assert response["type"] == "page_add"
    assert response["page"] == "test_page_type"
    assert response["parameters"]["test_param"] == 1

    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.websockets
async def test_core_consumer_add_page_doesnt_exist(data_fixture):
    # When trying to subscribe to not existing page
    # we do not expect the confirmation
    communicator = WebsocketCommunicator(
        application,
        f"ws/core/?jwt_token={ANONYMOUS_USER_TOKEN}",
        headers=[(b"origin", b"http://localhost")],
    )
    await communicator.connect()
    await communicator.receive_json_from()

    await communicator.send_json_to({"page": "doesnt_exist", "test_param": 1})
    assert communicator.output_queue.qsize() == 0
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.websockets
async def test_core_consumer_add_to_page_failure(data_fixture, test_page_types):
    user_1, token_1 = data_fixture.create_user_and_token()
    communicator = WebsocketCommunicator(
        application,
        f"ws/core/?jwt_token={token_1}",
        headers=[(b"origin", b"http://localhost")],
    )
    await communicator.connect()
    await communicator.receive_json_from()

    # Page that will return False from can_add()
    # won't send the confirmation
    await communicator.send_json_to(
        {"page": "test_page_type_not_accepting", "test_param": 1}
    )
    assert communicator.output_queue.qsize() == 0

    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.websockets
async def test_core_consumer_remove_page_success(data_fixture, test_page_types):
    user_1, token_1 = data_fixture.create_user_and_token()
    communicator = WebsocketCommunicator(
        application,
        f"ws/core/?jwt_token={token_1}",
        headers=[(b"origin", b"http://localhost")],
    )
    await communicator.connect()
    await communicator.receive_json_from()

    await communicator.send_json_to({"page": "test_page_type", "test_param": 1})
    response = await communicator.receive_json_from(timeout=0.1)

    await communicator.send_json_to({"remove_page": "test_page_type", "test_param": 1})
    response = await communicator.receive_json_from(timeout=0.1)

    assert response["type"] == "page_discard"
    assert response["page"] == "test_page_type"
    assert response["parameters"]["test_param"] == 1

    # Removing a page will send a confirmation again
    # even if it is unsubscribed already
    await communicator.send_json_to({"remove_page": "test_page_type", "test_param": 1})
    response = await communicator.receive_json_from(timeout=0.1)

    assert response["type"] == "page_discard"
    assert response["page"] == "test_page_type"
    assert response["parameters"]["test_param"] == 1

    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.websockets
async def test_core_consumer_remove_page_doesnt_exist(data_fixture):
    # When trying to unsubscribe from not existing page
    # we do not expect the confirmation
    communicator = WebsocketCommunicator(
        application,
        f"ws/core/?jwt_token={ANONYMOUS_USER_TOKEN}",
        headers=[(b"origin", b"http://localhost")],
    )
    await communicator.connect()
    await communicator.receive_json_from()

    await communicator.send_json_to({"page_remove": "doesnt_exist", "test_param": 1})
    assert communicator.output_queue.qsize() == 0
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.websockets
async def test_get_page_context(data_fixture, test_page_types):
    page_type = test_page_types[0]
    user_1, token_1 = data_fixture.create_user_and_token()
    consumer = CoreConsumer()
    consumer.scope = {}
    consumer.scope["user"] = user_1
    consumer.scope["web_socket_id"] = 234
    content = {
        "page": page_type.type,
        "test_param": 2,
    }
    result = await consumer.get_page_context(content, "page")
    assert result == PageContext(
        page_type=page_type,
        parameters={"test_param": 2},
        user=user_1,
        web_socket_id=234,
    )

    # Not existing page type
    content = {
        "page": "doesnt_exist",
        "test_param": 2,
    }
    result = await consumer.get_page_context(content, "page")
    assert result is None

    # Missing user
    consumer.scope["user"] = None
    content = {
        "page": page_type.type,
        "test_param": 2,
    }
    result = await consumer.get_page_context(content, "page")
    assert result is None


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@pytest.mark.websockets
async def test_core_consumer_remove_all_page_scopes(data_fixture, test_page_types):
    user_1, token_1 = data_fixture.create_user_and_token()
    scope_1 = PageScope("test_page_type", {"test_param": 1})
    scope_2 = PageScope("test_page_type", {"test_param": 2})
    pages = SubscribedPages()
    pages.add(scope_1)
    pages.add(scope_2)

    consumer = CoreConsumer()
    consumer.scope = {"pages": pages, "user": user_1, "web_socket_id": 123}
    consumer.channel_name = "test_channel_name"
    consumer.channel_layer = AsyncMock()

    async def base_send(message):
        pass

    consumer.base_send = base_send

    assert len(consumer.scope["pages"]) == 2

    await consumer.remove_all_page_scopes()

    assert len(consumer.scope["pages"]) == 0


# SubscribedPages


@pytest.mark.websockets
def test_subscribed_pages_adds_page_without_duplicates():
    scope_1 = PageScope("test_page_type", {"test_param": 1})
    scope_2 = PageScope("test_page_type", {"test_param": 2})
    scope_3 = PageScope("test_page_type_not_accepting", {"test_param": 1})
    scope_4 = PageScope("test_page_type", {"test_param": 1})
    pages = SubscribedPages()

    pages.add(scope_1)
    pages.add(scope_2)
    pages.add(scope_3)
    pages.add(scope_4)

    assert len(pages) == 3


@pytest.mark.websockets
def test_subscribed_pages_removes_pages_by_parameters():
    scope_1 = PageScope("test_page_type", {"test_param": 1})
    scope_2 = PageScope("test_page_type", {"test_param": 2})
    scope_3 = PageScope("test_page_type", {"test_param": 3})
    pages = SubscribedPages()

    pages.add(scope_1)
    pages.add(scope_2)
    pages.add(scope_3)

    assert len(pages) == 3

    pages.remove(scope_2)

    assert scope_1 in pages.pages
    assert scope_2 not in pages.pages
    assert scope_3 in pages.pages


@pytest.mark.websockets
def test_subscribed_pages_removes_pages_without_error():
    scope_1 = PageScope("test_page_type", {"test_param": 1})
    scope_2 = PageScope("test_page_type", {"test_param": 2})
    pages = SubscribedPages()

    pages.add(scope_1)
    pages.add(scope_2)

    assert len(pages) == 2

    # should not throw error
    pages.remove(scope_1)
    pages.remove(scope_1)
    pages.remove(scope_2)
    pages.remove(scope_2)

    assert len(pages) == 0
