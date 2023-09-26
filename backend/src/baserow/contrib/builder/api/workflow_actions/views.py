from typing import Dict

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from baserow.api.decorators import validate_body_custom_fields
from baserow.contrib.builder.api.workflow_actions.serializers import (
    BuilderWorkflowActionSerializer,
    CreateBuilderWorkflowActionSerializer,
)
from baserow.contrib.builder.elements.handler import ElementHandler
from baserow.contrib.builder.workflow_actions.registries import (
    builder_workflow_action_type_registry,
)
from baserow.contrib.builder.workflow_actions.service import (
    BuilderWorkflowActionService,
)
from rest_framework.response import Response


class BuilderWorkflowActionsView(APIView):
    permission_classes = (IsAuthenticated,)

    @validate_body_custom_fields(
        builder_workflow_action_type_registry,
        base_serializer_class=CreateBuilderWorkflowActionSerializer,
    )
    def post(self, request, data: Dict, element_id: int):
        type_name = data.pop("type")
        workflow_action_type = builder_workflow_action_type_registry.get(type_name)
        element = ElementHandler().get_element(element_id)

        workflow_action = BuilderWorkflowActionService().create_workflow_action(
            request.user, workflow_action_type, element, **data
        )

        serializer = builder_workflow_action_type_registry.get_serializer(
            workflow_action, BuilderWorkflowActionSerializer
        )

        return Response(serializer.data)
