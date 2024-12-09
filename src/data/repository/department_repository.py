from ..db import DB
from .base_repository import BaseRepository
from ..filter import Filter
from typing import List


class DepartmentRepository(BaseRepository):
    """
    Repository for managing department records.
    """

    def __init__(self, db: DB):
        super().__init__(db, "departments")

    def get_joins(self):
        # no joins needed
        return """
        """

    def get_mappings(self):
        mappings = {
            "id": "departments.id",
            "name": "departments.name",
            "research_areas": "departments.research_areas",
        }
        return mappings

    def search_staff(
        self,
        filter: Filter = None,
        fields: List[str] = None,
        limit: int = None,
        orderBy: str = None,
    ):
        """
        Search for staff records based on department.
        The academic and non academic staff are merged into a single entity
        using UNION ALL. Filters are only applied to the department.
        Aggregations do not work for this method

        :param filter: Filter object containing conditions.
        :param fields: List of fields to select.
        :return: List of records matching the filter.
        """
        if not fields:
            fields = ["*"]
        filter_query = f"SELECT {self.table}.* FROM {self.table}"

        where_clause, _, params = filter.compile() if filter else (None, None, None)

        if where_clause:
            filter_query += f" WHERE {where_clause}"

        # There's no easy way to do this. I've tried working it
        # out using UNION ALL and WITH / subselect
        with_query = f"""
        WITH filtered_departments as (
            {filter_query}
        )
        """

        query = f"""
            {with_query}
            SELECT a.id, a.name, fd.id as department_id, fd.name as department_name, TRUE AS academic_staff
            FROM lecturers AS a
            JOIN filtered_departments AS fd ON a.department_id = fd.id
            UNION ALL
            SELECT b.id, b.name, fd.id as department_id, fd.name as department_name, FALSE AS academic_staff
            FROM non_academic_staff AS b
            JOIN filtered_departments AS fd ON b.department_id = fd.id;
        """

        if orderBy:
            query += f" ORDER BY {orderBy}"

        if limit:
            query += f" LIMIT {limit}"

        return self.db.execute_query(query, params)
