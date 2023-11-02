from rest_framework import serializers

from baserow.api.applications.serializers import ApplicationSerializer
from baserow.contrib.database.api.tables.serializers import TableSerializer
from baserow.contrib.database.views.models import View


class LocalBaserowViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = View
        fields = ("id", "table_id", "name")


class LocalBaserowDatabaseSerializer(ApplicationSerializer):
    tables = TableSerializer(
        many=True,
        help_text="This field is specific to the `database` application and contains "
        "an array of tables that are in the database.",
    )
    views = LocalBaserowViewSerializer(
        many=True,
        help_text="This field is specific to the `database` application and contains "
        "an array of views that are in the tables.",
    )

    class Meta(ApplicationSerializer.Meta):
        ref_name = "DatabaseApplication"
        fields = ApplicationSerializer.Meta.fields + ("tables", "views")


class LocalBaserowContextDataSerializer(serializers.Serializer):
    databases = LocalBaserowDatabaseSerializer(many=True)
