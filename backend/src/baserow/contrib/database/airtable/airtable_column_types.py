from datetime import datetime
from decimal import Decimal

from django.core.exceptions import ValidationError

from baserow.contrib.database.fields.registries import field_type_registry
from baserow.contrib.database.fields.models import (
    NUMBER_TYPE_INTEGER,
    NUMBER_TYPE_DECIMAL,
    TextField,
    LongTextField,
    URLField,
    NumberField,
    RatingField,
    BooleanField,
    DateField,
    LastModifiedField,
    CreatedOnField,
    LinkRowField,
    EmailField,
    FileField,
    SingleSelectField,
    MultipleSelectField,
    PhoneNumberField,
)

from .helpers import import_airtable_date_type_options, set_select_options_on_field
from .registry import AirtableColumnType


class TextAirtableColumnType(AirtableColumnType):
    type = "text"

    def to_baserow_field(self, raw_airtable_column):
        validator_name = raw_airtable_column.get("typeOptions", {}).get("validatorName")
        if validator_name == "url":
            return URLField()
        elif validator_name == "email":
            return EmailField()
        else:
            return TextField()

    def to_baserow_export_serialized_value(
        self,
        row_id_mapping,
        raw_airtable_column,
        baserow_field,
        value,
        files_to_download,
    ):
        if isinstance(baserow_field, (EmailField, URLField)):
            try:
                field_type = field_type_registry.get_by_model(baserow_field)
                field_type.validator(value)
            except ValidationError:
                return ""

        return value


class MultilineTextAirtableColumnType(AirtableColumnType):
    type = "multilineText"

    def to_baserow_field(self, raw_airtable_column):
        return LongTextField()


class RichTextTextAirtableColumnType(AirtableColumnType):
    type = "richText"

    def to_baserow_field(self, raw_airtable_column):
        return LongTextField()

    def to_baserow_export_serialized_value(
        self,
        row_id_mapping,
        raw_airtable_column,
        baserow_field,
        value,
        files_to_download,
    ):
        return "".join([v["insert"] for v in value["documentValue"]])


class NumberAirtableColumnType(AirtableColumnType):
    type = "number"

    def to_baserow_field(self, raw_airtable_column):
        type_options = raw_airtable_column.get("typeOptions", {})

        return NumberField(
            number_type=NUMBER_TYPE_DECIMAL
            if type_options.get("format", "integer") == "decimal"
            else NUMBER_TYPE_INTEGER,
            number_decimal_places=max(1, type_options.get("precision", 1)),
            number_negative=type_options.get("negative", True),
        )

    def to_baserow_export_serialized_value(
        self,
        row_id_mapping,
        raw_airtable_column,
        baserow_field,
        value,
        files_to_download,
    ):
        if value is not None:
            value = Decimal(value)

        if value is not None and not baserow_field.number_negative and value < 0:
            value = None

        return None if value is None else str(value)


class RatingAirtableColumnType(AirtableColumnType):
    type = "rating"

    def to_baserow_field(self, values):
        return RatingField(max_value=values.get("typeOptions", {}).get("max", 5))


class CheckboxAirtableColumnType(AirtableColumnType):
    type = "checkbox"

    def to_baserow_field(self, raw_airtable_column):
        return BooleanField()

    def to_baserow_export_serialized_value(
        self,
        row_id_mapping,
        raw_airtable_column,
        baserow_field,
        value,
        files_to_download,
    ):
        return "true" if value else "false"


class DateAirtableColumnType(AirtableColumnType):
    type = "date"

    def to_baserow_field(self, raw_airtable_column):
        type_options = raw_airtable_column.get("typeOptions", {})
        return DateField(**import_airtable_date_type_options(type_options))

    def to_baserow_export_serialized_value(
        self,
        row_id_mapping,
        raw_airtable_column,
        baserow_field,
        value,
        files_to_download,
    ):
        if value is None:
            return value

        value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")

        if baserow_field.date_include_time:
            return f"{value.isoformat()}+00:00"
        else:
            return value.strftime("%Y-%m-%d")


class FormulaAirtableColumnType(AirtableColumnType):
    type = "formula"

    def to_baserow_field(self, raw_airtable_column):
        type_options = raw_airtable_column.get("typeOptions", {})
        display_type = type_options.get("displayType", "")
        if display_type == "lastModifiedTime":
            return LastModifiedField(
                timezone="UTC", **import_airtable_date_type_options(type_options)
            )
        elif display_type == "createdTime":
            return CreatedOnField(
                timezone="UTC", **import_airtable_date_type_options(type_options)
            )

    def to_baserow_export_serialized_value(
        self,
        row_id_mapping,
        raw_airtable_column,
        baserow_field,
        value,
        files_to_download,
    ):
        if isinstance(baserow_field, (CreatedOnField, LastModifiedField)):
            return None


class ForeignKeyAirtableColumnType(AirtableColumnType):
    type = "foreignKey"

    def to_baserow_field(self, raw_airtable_column):
        type_options = raw_airtable_column.get("typeOptions", {})
        return LinkRowField(
            link_row_table_id=type_options.get("foreignTableId"),
            link_row_related_field_id=type_options.get("symmetricColumnId"),
        )

    def to_baserow_export_serialized_value(
        self,
        row_id_mapping,
        raw_airtable_column,
        baserow_field,
        value,
        files_to_download,
    ):
        foreign_table_id = raw_airtable_column["typeOptions"]["foreignTableId"]
        return [row_id_mapping[foreign_table_id][v["foreignRowId"]] for v in value]


class MultipleAttachmentAirtableColumnType(AirtableColumnType):
    type = "multipleAttachment"

    def to_baserow_field(self, raw_airtable_column):
        return FileField()

    def to_baserow_export_serialized_value(
        self,
        row_id_mapping,
        raw_airtable_column,
        baserow_field,
        value,
        files_to_download,
    ):
        new_value = []
        for file in value:
            file_name = "_".join(file["url"].split("/")[-3:])
            files_to_download[file_name] = file["url"]
            new_value.append(
                {
                    "name": file_name,
                    "visible_name": file["filename"],
                    "original_name": file["filename"],
                }
            )

        return new_value


class SelectAirtableColumnType(AirtableColumnType):
    type = "select"

    def to_baserow_field(self, raw_airtable_column):
        field = SingleSelectField()
        field = set_select_options_on_field(
            field, raw_airtable_column.get("typeOptions", {})
        )
        return field


class MultiSelectAirtableColumnType(AirtableColumnType):
    type = "multiSelect"

    def to_baserow_field(self, raw_airtable_column):
        field = MultipleSelectField()
        field = set_select_options_on_field(
            field, raw_airtable_column.get("typeOptions", {})
        )
        return field


class PhoneAirtableColumnType(AirtableColumnType):
    type = "phone"

    def to_baserow_field(self, raw_airtable_column):
        return PhoneNumberField()

    def to_baserow_export_serialized_value(
        self,
        row_id_mapping,
        raw_airtable_column,
        baserow_field,
        value,
        files_to_download,
    ):
        try:
            field_type = field_type_registry.get_by_model(baserow_field)
            field_type.validator(value)
            return value
        except ValidationError:
            return ""
