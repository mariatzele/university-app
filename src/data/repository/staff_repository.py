from ..db import DB
from .base_repository import BaseRepository
from ..filter import Filter
from typing import List
import sqlparse


class StaffRepository(BaseRepository):
    """
    Repository for managing staff records.
    """

    def __init__(self, db: DB):
        # there's actually no staff table, we create it using UNION ALL
        # and override the search method
        super().__init__(db, "staff")

    def get_field_mappings(self):
        mappings = {
            "ID": "staff.id",
            "Name": "staff.name",
            "Department": "staff.department_name",
            "Academic staff": f"{self.field_to_boolean("staff.academic_staff", "YES", "NO")}",
        }
        return mappings

    def get_filter_mappings(self):
        mappings = {
            "id": "staff.id",
            "name": "staff.name",
            "department_id": "staff.department_id",
            "department_name": "staff.department_name",
            "academic_staff": "staff.academic_staff",
        }
        return mappings

    def search(
        self,
        filter: Filter = None,
        fields: List[str] = None,
        limit: int = None,
        orderBy: str = None,
    ):
        """
        Search for staff records based on department.
        The academic and non academic staff are merged into a single entity
        using UNION ALL. Filters are only applied to the union.
        Aggregations do not quite work for this method

        :param filter: Filter object containing conditions.
        :param fields: List of fields to select.
        :return: List of records matching the filter.
        """
        if not fields:
            fields = [f"{self.table}.*"]

        where_clause, _, params = filter.compile() if filter else (None, None, None)

        # There's no easy way to do this. I've tried working it
        # out using UNION ALL
        sub_query = f"""
            SELECT a.id, a.name, d.id as department_id, d.name as department_name, TRUE AS academic_staff
            FROM lecturers AS a
            JOIN departments AS d ON a.department_id = d.id
            UNION ALL
            SELECT b.id, b.name, d.id as department_id, d.name as department_name, FALSE AS academic_staff
            FROM non_academic_staff AS b
            JOIN departments AS d ON b.department_id = d.id
        """
        query = (
            f"SELECT DISTINCT {', '.join(fields)} FROM ({sub_query}) as {self.table}"
        )
        if where_clause:
            query += f" WHERE {where_clause}"

        if orderBy:
            query += f" ORDER BY {orderBy}"

        if limit:
            query += f" LIMIT {limit}"

        print("==================")
        print("Executing Query: ")
        print(sqlparse.format(query, reindent=True, keyword_case="upper"))
        print("==================")

        return self.db.execute_query(query, params)
