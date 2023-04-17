import re
from typing import TYPE_CHECKING, Dict

from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector
from django.db import connection

from psycopg2 import sql

from baserow.contrib.database.fields.models import Field
from baserow.contrib.database.table.cache import invalidate_table_in_model_cache

if TYPE_CHECKING:
    from baserow.contrib.database.table.models import Table

RE_SPACE = re.compile(r"[\s]+", re.UNICODE)
RE_POSTGRES_ESCAPE_CHARS = re.compile(r"[&:(|)!><]", re.UNICODE)


def get_vector_column_name(source_field_db_column: str) -> str:
    return f"{source_field_db_column}_tsv"


def get_vector_index_name(table: "Table", source_field_name: str) -> str:
    source_table = table.get_database_table_name()
    tsv_db_column: str = get_vector_column_name(source_field_name)
    return f"tbl_{source_table}_{tsv_db_column}_idx"


class SearchHandler:
    """ """

    def update_vector_row(
        self, table: "Table", value_field_map: Dict[str, Field]
    ) -> None:
        """ """

        model = table.get_model()

        vector_updates = {}
        for field_name, field_model in value_field_map.items():
            if not field_model.searchable:
                print(f"Field {field_model.db_column} is not searchable, skipping it.")
                continue

            vector_updates[get_vector_column_name(field_name)] = SearchVector(
                field_name
            )

        model.objects.update(**vector_updates)
        print(f"Updated tsvector columns {', '.join(vector_updates.keys())}")

    def create_vector_column(self, table: "Table", source_field_name: str) -> None:
        """
        Responsible for creating a `tsvector` for field that was created.
        """
        raw_sql = """
            ALTER TABLE {source_table}
            ADD COLUMN {tsv_column} tsvector;
            UPDATE {source_table}
            SET {tsv_column} = to_tsvector({source_column});
            CREATE INDEX {tsv_index}
            ON {source_table} USING GIN ({tsv_column});
        """
        tsv_db_column: str = get_vector_column_name(source_field_name)
        tsv_index = table.get_collision_safe_field_tsv_idx_name(tsv_db_column)
        with connection.cursor() as cursor:
            cursor.execute(
                sql.SQL(raw_sql).format(
                    tsv_index=sql.Identifier(tsv_index),
                    tsv_column=sql.Identifier(tsv_db_column),
                    source_table=sql.Identifier(table.get_database_table_name()),
                    source_column=sql.Identifier(source_field_name),
                )
            )
        invalidate_table_in_model_cache(table.id)
        print(f"Creating tsvector {tsv_db_column}")

    def remove_vector_column(self, table: "Table", source_field_name: str):
        """
        Responsible for removing a `tsvector` field when its corresponding
        field has been dropped.
        """
        with connection.schema_editor() as schema_editor:
            table_model = table.get_model()
            tsv_db_column = get_vector_column_name(source_field_name)
            tsv_index = table.get_collision_safe_field_tsv_idx_name(tsv_db_column)
            tsvector_field = table_model._meta.get_field(tsv_db_column)
            schema_editor.remove_field(table_model, tsvector_field)
            schema_editor.remove_index(
                table_model, GinIndex(name=tsv_index, fields=[tsv_db_column])
            )
        invalidate_table_in_model_cache(table.id)
        print(f"Removing tsvector {tsv_db_column}")
