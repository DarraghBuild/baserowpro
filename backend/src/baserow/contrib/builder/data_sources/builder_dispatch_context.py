from baserow.contrib.builder.data_providers.registries import (
    builder_data_provider_type_registry,
)
from baserow.core.services.dispatch_context import DispatchContext


class BuilderDispatchContext(DispatchContext):
    def __init__(self, request, page):
        self.request = request
        self.page = page

        super().__init__()

    @property
    def data_provider_registry(self):
        return builder_data_provider_type_registry

    def range(self, service):
        """Return page range from the GET parameters."""

        return [
            int(self.request.GET.get("offset", 0)),
            int(self.request.GET.get("count", 20)),
        ]
