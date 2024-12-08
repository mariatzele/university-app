from ..db import DB
from .base_repository import BaseRepository


class StudentRepository(BaseRepository):
    """
    Repository for managing student records.
    """

    def __init__(self, db: DB):
        super().__init__(db, "students")

    def get_joins(self):
        return """
            LEFT JOIN student_enrollments ON students.id = student_enrollments.student_id
            LEFT JOIN lecturers on students.advised_by_lecturer_id = lecturers.id
            LEFT JOIN courses ON student_enrollments.course_id = courses.id
        """
