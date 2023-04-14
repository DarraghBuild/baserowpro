from rest_framework import serializers


class FullHealthCheckSerializer(serializers.Serializer):
    passing = serializers.BooleanField(
        read_only=True,
        help_text="False if any of the critical service health checks are failing, "
        "true otherwise.",
    )
    checks = serializers.DictField(
        read_only=True,
        child=serializers.CharField(),
        help_text="An object keyed by the name of the "
        "health check and the value being "
        "the result.",
    )
