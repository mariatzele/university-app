from ..db import DB
from ..filter import Filter
from typing import List
import sqlparse


class BaseRepository:
    """
    A base repository that provides common database operations for entities.
    """

    def __init__(self, db: DB, table: str):
        self.db = db
        self.table = table

    def get(self, filter: Filter):
        result = self.search(filter)
        return result[0] if result else None

    def map_fields(self, fields):

        mappings = self.get_field_mappings()
        return [
            f"{mappings[field]} as `{field}`" for field in fields if field in mappings
        ]

    def map_filters(self, filters):
        mappings = self.get_filter_mappings()
        return {mappings[key]: value for key, value in filters.items()}

    def search(
        self,
        filter: Filter = None,
        fields: List[str] = None,
        limit: int = None,
        orderBy: str = None,
    ):
        """
        Search for records based on a filter.

        :param filter: Filter object containing conditions.
        :param fields: List of fields to select.
        :return: List of records matching the filter.
        """
        joins = self.get_joins()
        if not fields:
            fields = [f"{self.table}.*"]

        # Important! Use DISTINCT here because we do left joins later and may end up with duplicates
        # this is a bit more expensive to run but it's OK because the database is small
        query = f"SELECT DISTINCT {', '.join(fields)} FROM {self.table} {joins}"

        where_clause, having_clause, params = (
            filter.compile() if filter else (None, None, None)
        )

        if where_clause:
            query += f" WHERE {where_clause}"

        # Important! always group by the main table entity to allow for aggregations in the fields param
        query += f" GROUP BY {self.table}.id"
        if having_clause:
            query += f" {having_clause}"

        if orderBy:
            query += f" ORDER BY {orderBy}"

        if limit:
            query += f" LIMIT {limit}"

        # Log queries before being executed - helps for debugging
        print("==================")
        print("Executing Query: ")
        print(sqlparse.format(query, reindent=True, keyword_case="upper"))
        print("==================")
        return self.db.execute_query(query, params)

    def get_joins(self):
        """
        Method to be overridden in child classes to define specific JOIN logic.
        """
        return ""  # By default, no joins are added. Child classes should override this.

    def get_field_mappings(self):
        mappings = {}  # no mappings by default
        return mappings

    def get_filter_mappings(self):
        return self.get_field_mappings()

    def get_column_names(self):
        return list(self.get_field_mappings().keys())

    def field_to_boolean(self, field_name, true_value, false_value):
        return f"""
        CASE 
            WHEN {field_name} = TRUE THEN '{true_value}'
            WHEN {field_name} = FALSE THEN '{false_value}'
            ELSE 'unknown'
        END
        """
