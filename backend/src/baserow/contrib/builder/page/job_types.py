from typing import Any, Dict

from django.contrib.auth.models import AbstractUser
from django.db import transaction

from baserow.contrib.builder.api.pages.serializers import PageSerializer
from baserow.contrib.builder.page.handler import PageHandler
from baserow.contrib.builder.page.models import DuplicatePageJob
from baserow.contrib.builder.page.operations import DuplicatePageOperationType
from baserow.contrib.builder.page.serivce import PageService
from baserow.core.handler import CoreHandler
from baserow.core.jobs.registries import JobType
from rest_framework import serializers


class DuplicatePageJobType(JobType):
    type = "duplicate_page"
    model_class = DuplicatePageJob
    max_count = 1

    request_serializer_field_names = ["page_id"]

    request_serializer_field_overrides = {
        "page_id": serializers.IntegerField(
            help_text="The ID of the page to duplicate.",
        ),
    }

    serializer_field_names = ["original_page", "duplicated_page"]
    serializer_field_overrides = {
        "original_page": PageSerializer(read_only=True),
        "duplicated_page": PageSerializer(read_only=True),
    }

    def transaction_atomic_context(self, job: "DuplicatePageJobType"):
        return transaction.atomic()

    def prepare_values(
        self, values: Dict[str, Any], user: AbstractUser
    ) -> Dict[str, Any]:
        page = PageHandler().get_page(values.pop("page_id"))

        CoreHandler().check_permissions(
            user,
            DuplicatePageOperationType.type,
            group=page.builder.group,
            context=page,
        )

        return {"original_page": page}

    def run(self, job, progress):
        new_page_clone = PageService().duplicate_page()

        job.duplicated_page = new_page_clone
        job.save(update_fields=("duplicated_page",))

        return new_page_clone
