from ..db import DB
from ..filter import Filter
from typing import List


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

        return self.db.execute_query(query, params)

    def get_joins(self):
        """
        Method to be overridden in child classes to define specific JOIN logic.
        """
        return ""  # By default, no joins are added. Child classes should override this.
