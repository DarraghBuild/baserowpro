from rest_framework import serializers

from baserow.contrib.integrations.local_baserow.models import (
    LocalBaserowTableServiceFilter,
)


class LocalBaserowTableServiceFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalBaserowTableServiceFilter
        fields = ("id", "service", "field", "type", "value")


class LocalBaserowTableServiceSerializerMixin(serializers.Serializer):
    service_id = serializers.IntegerField(
        source="id", required=False, help_text="The id of the Baserow service."
    )
