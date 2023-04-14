from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from baserow.api.health.serializers import FullHealthCheckSerializer
from baserow.core.health.handler import HealthCheckHandler


class FullHealthCheckView(APIView):
    permission_classes = (IsAdminUser,)

    @extend_schema(
        tags=["Health"],
        request=None,
        operation_id="full_health_check",
        description="Runs a full health check testing as many services and systems "
        "as possible. These health checks can be expensive operations such as writing "
        "files to storage etc.",
        responses={
            200: FullHealthCheckSerializer,
        },
    )
    def get(self, request: Request) -> Response:
        result = HealthCheckHandler.run_all_checks()
        return Response(
            FullHealthCheckSerializer(
                {"checks": result.checks, "passing": result.passing}
            ).data
        )
