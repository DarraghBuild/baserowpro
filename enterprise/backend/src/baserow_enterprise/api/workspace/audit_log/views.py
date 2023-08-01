from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import translation
from baserow.core.actions import DeleteWorkspaceActionType, OrderWorkspacesActionType
from baserow_enterprise.api.admin.audit_log.serializers import (
    AuditLogExportJobRequestSerializer,
    AuditLogExportJobResponseSerializer,
)

from baserow_premium.api.admin.views import APIListingView
from baserow_premium.license.handler import LicenseHandler
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED
from rest_framework.views import APIView

from baserow.api.decorators import (
    map_exceptions,
    validate_body,
    validate_query_parameters,
)
from baserow.api.jobs.errors import ERROR_MAX_JOB_COUNT_EXCEEDED
from baserow.api.jobs.serializers import JobSerializer
from baserow.api.schemas import CLIENT_SESSION_ID_SCHEMA_PARAMETER, get_error_schema
from baserow.core.action.registries import action_type_registry
from baserow.core.jobs.exceptions import MaxJobCountExceeded
from baserow.core.jobs.handler import JobHandler
from baserow.core.jobs.registries import job_type_registry
from baserow.core.models import Workspace
from baserow_enterprise.audit_log.job_types import AuditLogExportJobType
from baserow_enterprise.audit_log.models import AuditLogEntry
from baserow_enterprise.features import AUDIT_LOG

from .serializers import (
    AuditLogQueryParamsSerializer,
    AuditLogSerializer,
    AuditLogUserSerializer,
    AuditLogActionTypeSerializer,
)

User = get_user_model()


class WorkspaceAuditLogView(APIListingView):
    serializer_class = AuditLogSerializer
    filters_field_mapping = {
        "user_id": "user_id",
        "action_type": "action_type",
        "from_timestamp": "action_timestamp__gte",
        "to_timestamp": "action_timestamp__lte",
        "ip_address": "ip_address",
    }
    sort_field_mapping = {
        "user": "user_email",
        "type": "action_type",
        "timestamp": "action_timestamp",
        "ip_address": "ip_address",
    }
    default_order_by = "-action_timestamp"

    def get_queryset(self, request):
        return AuditLogEntry.objects.filter(workspace_id=self.kwargs["workspace_id"])

    def get_serializer(self, request, *args, **kwargs):
        return super().get_serializer(
            request, *args, context={"request": request}, **kwargs
        )

    @extend_schema(
        tags=["Admin"],
        operation_id="admin_audit_log",
        description="Lists all audit log entries for the given workspace id.",
        **APIListingView.get_extend_schema_parameters(
            "audit_log_entries", serializer_class, [], sort_field_mapping
        ),
    )
    @validate_query_parameters(AuditLogQueryParamsSerializer)
    def get(self, request, workspace_id: int, query_params):
        self.workspace_id = workspace_id
        with translation.override(request.user.profile.language):
            return super().get(request)


class AuditLogActionTypeFilterView(APIView):
    serializer_class = AuditLogActionTypeSerializer
    exclude_types = [
        DeleteWorkspaceActionType.type,
        OrderWorkspacesActionType.type,
    ]

    def filter_action_types(self, action_types, search):
        search_lower = search.lower()
        return [
            action_type
            for action_type in action_types
            if search_lower in action_type["value"].lower()
        ]

    @extend_schema(
        tags=["Workspace"],
        operation_id="workspace_audit_log_types",
        description="List all distinct action types related to an audit log entry.",
    )
    def get(self, request, workspace_id: int):
        # Since action's type is translated at runtime and there aren't that
        # many, we can fetch them all and filter them in memory to match the
        # search query on the translated value.
        with translation.override(request.user.profile.language):
            search = request.GET.get("search")

            filtered_action_types = [
                action_type
                for action_type in action_type_registry.get_all()
                if action_type.type not in self.exclude_types
            ]

            action_types = AuditLogActionTypeSerializer(
                filtered_action_types, many=True
            ).data

            if search:
                action_types = self.filter_action_types(action_types, search)

            return Response(
                {
                    "count": len(action_types),
                    "next": None,
                    "previous": None,
                    "results": sorted(action_types, key=lambda x: x["value"]),
                }
            )


class AuditLogUserFilterView(APIListingView):
    serializer_class = AuditLogUserSerializer
    search_fields = ["email"]
    default_order_by = "email"

    def get_queryset(self, request):
        return User.objects.filter(workspaceuser__workspace_id=self.workspace_id)

    @extend_schema(
        tags=["Workspace"],
        operation_id="workspace_audit_log_users",
        description="List all users that have performed an action in the audit log.",
        **APIListingView.get_extend_schema_parameters(
            "users", serializer_class, search_fields, {}
        ),
    )
    def get(self, request, workspace_id: int):
        self.workspace_id = workspace_id
        return super().get(request)


class AsyncAuditLogExportView(APIView):
    @extend_schema(
        parameters=[CLIENT_SESSION_ID_SCHEMA_PARAMETER],
        tags=["Audit log export"],
        operation_id="export_audit_log",
        description=("Creates a job to export the filtered audit log to a CSV file."),
        request=AuditLogExportJobRequestSerializer,
        responses={
            202: AuditLogExportJobResponseSerializer,
            400: get_error_schema(
                ["ERROR_REQUEST_BODY_VALIDATION", "ERROR_MAX_JOB_COUNT_EXCEEDED"]
            ),
        },
    )
    @transaction.atomic
    @map_exceptions({MaxJobCountExceeded: ERROR_MAX_JOB_COUNT_EXCEEDED})
    @validate_body(AuditLogExportJobRequestSerializer)
    def post(self, request, workspace_id, data):
        """Creates a job to export the filtered audit log entries to a CSV file."""

        data["filter_workspace_id"] = workspace_id

        csv_export_job = JobHandler().create_and_start_job(
            request.user, AuditLogExportJobType.type, **data
        )

        serializer = job_type_registry.get_serializer(
            csv_export_job, JobSerializer, context={"request": request}
        )
        return Response(serializer.data, status=HTTP_202_ACCEPTED)
