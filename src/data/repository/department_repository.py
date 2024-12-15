"""department_repository.py"""
from ..db import DB
from .base_repository import BaseRepository


class DepartmentRepository(BaseRepository):
    """
    Repository for managing department records.
    """

    def __init__(self, db: DB):
        super().__init__(db, "departments")

    def get_field_mappings(self):
        """
        returns a dictionary that maps human-readable field names to SQL
        database fields
        """
        mappings = {
            "ID": "departments.id",
            "Name": "departments.name",
            "Research areas": "departments.research_areas",
        }
        return mappings

    def get_filter_mappings(self):
        """
        returns a dictionary that maps filter values to SQL
        database fields
        """
        mappings = {
            "id": "departments.id",
            "name": "departments.name",
            "research_areas": "departments.research_areas",
        }
        return mappings
