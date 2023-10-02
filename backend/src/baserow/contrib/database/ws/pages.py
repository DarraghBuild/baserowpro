from django.conf import settings

from baserow.contrib.database.table.exceptions import TableDoesNotExist
from baserow.contrib.database.table.handler import TableHandler
from baserow.contrib.database.table.operations import (
    ListenToAllDatabaseTableEventsOperationType,
)
from baserow.contrib.database.views.exceptions import (
    NoAuthorizationToPubliclySharedView,
    ViewDoesNotExist,
)
from baserow.contrib.database.views.handler import ViewHandler
from baserow.contrib.database.views.registries import view_type_registry
from baserow.core.exceptions import PermissionDenied, UserNotInWorkspace
from baserow.core.handler import CoreHandler
from baserow.ws.registries import PageType
from baserow.ws.tasks import broadcast_to_channel_group
from baserow.contrib.database.rows.handler import RowHandler
from baserow.contrib.database.rows.exceptions import RowDoesNotExist

class TablePageType(PageType):
    type = "table"
    parameters = ["table_id"]

    def can_add(self, user, web_socket_id, table_id, **kwargs):
        """
        The user should only have access to this page if the table exists and if they
        have access to the table.
        """

        if not table_id:
            return False

        try:
            handler = TableHandler()
            table = handler.get_table(table_id)
            CoreHandler().check_permissions(
                user,
                ListenToAllDatabaseTableEventsOperationType.type,
                workspace=table.database.workspace,
                context=table,
            )
        except (UserNotInWorkspace, TableDoesNotExist, PermissionDenied):
            return False

        return True

    def get_group_name(self, table_id, **kwargs):
        return f"table-{table_id}"


class PublicViewPageType(PageType):
    type = "view"
    parameters = ["slug", "token"]

    def can_add(self, user, web_socket_id, slug, token=None, **kwargs):
        """
        The user should only have access to this page if the view exists and:
        - the user have access to the workspace
        - the view is public and not password protected
        - the view is public, password protected and the token provided is valid.
        """

        if settings.DISABLE_ANONYMOUS_PUBLIC_VIEW_WS_CONNECTIONS:
            return False

        if not slug:
            return False

        try:
            handler = ViewHandler()
            view = handler.get_public_view_by_slug(
                user, slug, authorization_token=token
            )
        except (ViewDoesNotExist, NoAuthorizationToPubliclySharedView):
            return False

        view_type = view_type_registry.get_by_model(view.specific_class)
        if not view_type.when_shared_publicly_requires_realtime_events:
            return False

        return True

    def get_group_name(self, slug, **kwargs):
        return f"view-{slug}"

    # TODO: remove? how is this called?
    # def broadcast_to_views(self, payload, view_slugs):
    #     for view_slug in view_slugs:
    #         self.broadcast(payload, ignore_web_socket_id=None, slug=view_slug)


class RowPageType(PageType):
    type = "row"
    parameters = ["table_id", "row_id"]

    def can_add(self, user, web_socket_id, table_id, row_id, **kwargs):
        """
        The user should only have access to this page if the table exists and if they
        have access to the table.
        """

        if not table_id:
            return False

        try:
            handler = TableHandler()
            table = handler.get_table(table_id)
            CoreHandler().check_permissions(
                user,
                ListenToAllDatabaseTableEventsOperationType.type,
                workspace=table.database.workspace,
                context=table,
            )
            row_handler = RowHandler()
            row_handler.get_row(user, table, row_id)
        except (UserNotInWorkspace, TableDoesNotExist, PermissionDenied, RowDoesNotExist):
            return False

        return True

    def get_group_name(self, table_id, row_id, **kwargs):
        return f"table-{table_id}-row-{row_id}"
    
    def broadcast(self, payload, ignore_web_socket_id=None, **kwargs):
        """
        Broadcasts a payload to everyone within the group.

        :param payload: A payload that must be broad casted to all the users in the
            group.
        :type payload:  dict
        :param ignore_web_socket_id: If provided then the payload will not be broad
            casted to that web socket id. This is often the sender.
        :type ignore_web_socket_id: Optional[str]
        :param kwargs: The additional parameters including their provided values.
        :type kwargs: dict
        """

        broadcast_to_channel_group.delay(
            self.get_group_name(**kwargs), payload, ignore_web_socket_id
        )
