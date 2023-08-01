from django.urls import re_path

from .views import (
    WorkspaceAuditLogView,
    AuditLogUserFilterView,
    AuditLogActionTypeFilterView,
    AsyncAuditLogExportView,
)

app_name = "baserow_enterprise.api.workspace_audit_log"

urlpatterns = [
    re_path(
        r"^$",
        WorkspaceAuditLogView.as_view(),
        name="list",
    ),
    re_path(r"users/$", AuditLogUserFilterView.as_view(), name="users"),
    re_path(
        r"action-types/$",
        AuditLogActionTypeFilterView.as_view(),
        name="action_types",
    ),
    re_path(r"export/$", AsyncAuditLogExportView.as_view(), name="export"),
]
