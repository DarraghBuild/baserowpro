from rest_framework import serializers


class HeadingElementConfigSerializer(serializers.Serializer):
    value = serializers.CharField(
        help_text="The label displayed in the header.", default=""
    )


class ParagraphElementConfigSerializer(serializers.Serializer):
    content = serializers.CharField(help_text="The paragraph content.", default="")
