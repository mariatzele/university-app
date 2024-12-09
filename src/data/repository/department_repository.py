from ..db import DB
from .base_repository import BaseRepository


class DepartmentRepository(BaseRepository):
    """
    Repository for managing department records.
    """

    def __init__(self, db: DB):
        super().__init__(db, "departments")

    def get_mappings(self):
        mappings = {
            "id": "departments.id",
            "name": "departments.name",
            "research_areas": "departments.research_areas",
        }
        return mappings
