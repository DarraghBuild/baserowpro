from django.apps import AppConfig

from baserow.core.registries import object_scope_type_registry, operation_type_registry


class BuilderConfig(AppConfig):
    name = "baserow.contrib.builder"

    def ready(self):
        from baserow.core.registries import application_type_registry

        from .application_types import BuilderApplicationType

        application_type_registry.register(BuilderApplicationType())

        from baserow.contrib.builder.object_scopes import BuilderObjectScopeType
        from baserow.contrib.builder.page.object_scopes import (
            BuilderPageObjectScopeType,
        )

        object_scope_type_registry.register(BuilderObjectScopeType())
        object_scope_type_registry.register(BuilderPageObjectScopeType())

        from baserow.contrib.builder.operations import (
            ListPagesBuilderOperationType,
            OrderPagesBuilderOperationType,
        )

        operation_type_registry.register(ListPagesBuilderOperationType())
        operation_type_registry.register(OrderPagesBuilderOperationType())

        from baserow.contrib.builder.page.operations import (
            CreatePageOperationType,
            DeletePageOperationType,
            DuplicatePageOperationType,
            ReadPageOperationType,
            UpdatePageOperationType,
            ExportPageOperationType,
        )

        operation_type_registry.register(CreatePageOperationType())
        operation_type_registry.register(DeletePageOperationType())
        operation_type_registry.register(UpdatePageOperationType())
        operation_type_registry.register(ReadPageOperationType())
        operation_type_registry.register(DuplicatePageOperationType())
        operation_type_registry.register(ExportPageOperationType())

        from baserow.contrib.builder.page.job_types import DuplicatePageJobType
        from baserow.core.jobs.registries import job_type_registry

        job_type_registry.register(DuplicatePageJobType())

        # The signals must always be imported last because they use the registries
        # which need to be filled first.
        import baserow.contrib.builder.ws.signals  # noqa: F403, F401
