from ..db import DB
from .base_repository import BaseRepository


class CourseRepository(BaseRepository):
    """
    Repository for managing course records.
    """

    def __init__(self, db: DB):
        super().__init__(db, "courses")

    def get_field_mappings(self):
        mappings = {
            "ID": "courses.id",
            "Name": "courses.name",
            "Description": "courses.description",
            "Department": "departments.name",
            "Lecturer": "lecturers.name",
            "Level": "courses.level",
            "Credits": "courses.credits",
            "Prerequisites": "courses.prerequisites",
            "Schedule": "courses.schedule",
        }
        return mappings

    def get_filter_mappings(self):
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
            LEFT JOIN departments on courses.department_id = departments.id
        """
