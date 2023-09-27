from typing import Optional
from operator import attrgetter
from dataclasses import dataclass
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import AbstractUser
from baserow.ws.registries import page_registry, PageType


@dataclass
class PageContext:
    """
    The context about a page and a user when the user
    intends to be subscribed or unsubscribed from
    getting changes relevant to the page.
    """
    
    web_socket_id: str
    user: Optional[AbstractUser]
    page_type: PageType
    parameters: dict[str, any]


@dataclass
class PageScope:
    """
    Represents one page that a user can be subscribed to.
    Different page parameters can be used to represent
    subscriptions to the same page types with different 
    values (e.g. being subscribed to a table page with 
    table_id=1 or table_id=2)
    """
    
    page_type: str
    page_parameters: dict[str, any]


class SubscribedPages:
    """
    Holds information about all pages a user is subscribed to.
    """

    def __init__(self):
        self.pages: list[PageScope] = []

    def add(self, page_scope: PageScope):
        if page_scope not in self.pages:
            print()
            print("adding")
            print(page_scope)
            print()
            self.pages.append(page_scope)

    def remove(self, page_scope: PageScope):
        if page_scope in self.pages:
            print()
            print("removing")
            print(page_scope)
            print()
            self.pages.remove(page_scope)

    def __len__(self):
        return len(self.pages)
    
    def __iter__(self):
        return iter(self.pages)


class CoreConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

        user = self.scope["user"]
        web_socket_id = self.scope["web_socket_id"]

        await self.send_json(
            {
                "type": "authentication",
                "success": user is not None,
                "web_socket_id": web_socket_id,
            }
        )

        if not user:
            await self.close()
            return

        self.scope["pages"] = SubscribedPages()
        await self.channel_layer.group_add("users", self.channel_name)

    async def receive_json(self, content, **parameters):
        if "page" in content:
            await self.add_page_scope(content)
        if "remove_page" in content:
            await self.remove_page_scope(content)

    async def get_page_context(self, content, page_name_attr: str) -> PageContext:
        user = self.scope["user"]
        web_socket_id = self.scope["web_socket_id"]

        try:
            page_type = page_registry.get(content[page_name_attr])
        except page_registry.does_not_exist_exception_class:
            return

        parameters = {
            parameter: content.get(parameter) for parameter in page_type.parameters
        }

        return PageContext(
            page_type=page_type,
            parameters=parameters,
            user=user,
            web_socket_id=web_socket_id,
        )

    async def add_page_scope(self, content):
        """
        Subscribes the connection to a page abstraction. Based on the provided the page
        type we can figure out to which page the connection wants to subscribe to. This
        is for example used when the users visits a page that they might want to
        receive real time updates for.

        :param content: The provided payload by the user. This should contain the page
            type and additional parameters.
        :type content: dict
        """

        context = await self.get_page_context(content, "page")
        user, web_socket_id, page_type, parameters = attrgetter(
            "user", "web_socket_id", "page_type", "parameters"
        )(context)

        if not user:
            return

        can_add = await database_sync_to_async(page_type.can_add)(
            user, web_socket_id, **parameters
        )

        if not can_add:
            return

        group_name = page_type.get_group_name(**parameters)
        await self.channel_layer.group_add(group_name, self.channel_name)

        page_scope = PageScope(page_type=page_type, page_parameters=parameters)
        self.scope["pages"].add(page_scope)

        await self.send_json(
            {"type": "page_add", "page": page_type.type, "parameters": parameters}
        )

    async def remove_page_scope(self, content, send_confirmation=True):
        context = await self.get_page_context(content, "remove_page")
        user, page_type, parameters = attrgetter(
            "user", "page_type", "parameters"
        )(context)

        if not user:
            return

        group_name = page_type.get_group_name(**parameters)
        await self.channel_layer.group_discard(group_name, self.channel_name)

        page_scope = PageScope(page_type=page_type, page_parameters=parameters)
        self.scope["pages"].remove(page_scope)

        if send_confirmation:
            await self.send_json(
                {
                    "type": "page_discard",
                    "page": page_type,
                    "parameters": parameters,
                }
            )

    async def broadcast_to_users(self, event):
        """
        Broadcasts a message to all the users that are in the provided user_ids list.
        Optionally the ignore_web_socket_id is ignored because that is often the
        sender. Also, if `send_to_all_users` is set to True then all users will be sent
        the payload regardless of `user_ids`, but `ignore_web_socket_id` will still
        be respected.

        :param event: The event containing the payload, user ids and the web socket
            id that must be ignored.
        :type event: dict
        """

        web_socket_id = self.scope["web_socket_id"]
        payload = event["payload"]
        user_ids = event["user_ids"]
        ignore_web_socket_id = event["ignore_web_socket_id"]
        send_to_all_users = event["send_to_all_users"]

        shouldnt_ignore = (
            not ignore_web_socket_id or ignore_web_socket_id != web_socket_id
        )
        if shouldnt_ignore and (self.scope["user"].id in user_ids or send_to_all_users):
            await self.send_json(payload)

    async def broadcast_to_users_individual_payloads(self, event):
        """
        Accepts a payload mapping and sends the payload as JSON if the user_id of the
        consumer is part of the mapping provided

        :param event: The event containing the payload mapping
        """

        web_socket_id = self.scope["web_socket_id"]

        payload_map = event["payload_map"]
        ignore_web_socket_id = event["ignore_web_socket_id"]

        user_id = str(self.scope["user"].id)

        shouldnt_ignore = (
            not ignore_web_socket_id or ignore_web_socket_id != web_socket_id
        )

        if shouldnt_ignore and user_id in payload_map:
            await self.send_json(payload_map[user_id])

    async def broadcast_to_group(self, event):
        """
        Broadcasts a message to all the users that are in the provided group name.

        :param event: The event containing the payload, group name and the web socket
            id that must be ignored.
        :type event: dict
        """

        web_socket_id = self.scope["web_socket_id"]
        payload = event["payload"]
        ignore_web_socket_id = event["ignore_web_socket_id"]

        if not ignore_web_socket_id or ignore_web_socket_id != web_socket_id:
            await self.send_json(payload)

    async def remove_user_from_group(self, event):
        user_ids_to_remove = event["user_ids_to_remove"]
        user_id = self.scope["user"].id

        if len(self.scope["pages"]) == 0:
            return

        # TODO: extract method
        if user_id in user_ids_to_remove:
            for page_scope in self.scope["pages"]:
                content = {
                    "user": self.scope["user"],
                    "web_socket_id": self.scope["web_socket_id"],
                    "remove_page": page_scope.page_type,
                    "parameters": page_scope.page_parameters,
                }
                await self.remove_page_scope(content, send_confirmation=True)

    async def disconnect(self, message):
        for page_scope in self.scope["pages"]:
                content = {
                    "user": self.scope["user"],
                    "web_socket_id": self.scope["web_socket_id"],
                    "remove_page": page_scope.page_type,
                    "parameters": page_scope.page_parameters,
                }
                await self.remove_page_scope(content, send_confirmation=True)

        await self.channel_layer.group_discard("users", self.channel_name)
