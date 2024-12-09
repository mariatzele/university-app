from ..db import DB
from .base_repository import BaseRepository


class CourseRepository(BaseRepository):
    """
    Repository for managing course records.
    """

    def __init__(self, db: DB):
        super().__init__(db, "courses")

    def get_joins(self):
        return """
            LEFT JOIN lecturers ON courses.lecturer_id = lecturers.id
        """
