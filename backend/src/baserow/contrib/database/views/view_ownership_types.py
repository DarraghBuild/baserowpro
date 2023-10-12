from django.contrib.auth.models import AbstractUser

from baserow.contrib.database.views.models import View
from baserow.contrib.database.views.registries import ViewOwnershipType


class CollaborativeViewOwnershipType(ViewOwnershipType):
    """
    Represents views that are shared between all users that can access
    a specific table.
    """

    type = "collaborative"

    def change_ownership_or_raise(self, user: AbstractUser, view: View) -> View:
        view.ownership_type = self.type
        view.owned_by = user
        return view
