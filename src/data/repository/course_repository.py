from ..db import DB
from .base_repository import BaseRepository


class CourseRepository(BaseRepository):
    """
    Repository for managing course records.
    """

    def __init__(self, db: DB):
        super().__init__(db, "courses")

    def get_mappings(self):
        mappings = {
            "id": "courses.id",
            "name": "courses.name",
            "description": "courses.description",
            "department_id": "courses.department_id",
            "lecturer_id": "courses.lecturer_id",
            "level": "courses.level",
            "credits": "courses.credits",
            "prerequisites": "courses.prerequisites",
            "schedule": "courses.schedule",
        }
        return mappings

    def get_joins(self):
        return """
            LEFT JOIN lecturers ON courses.lecturer_id = lecturers.id
        """
