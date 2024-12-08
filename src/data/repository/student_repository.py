from ..db import DB
from .base_repository import BaseRepository


class StudentRepository(BaseRepository):
    """
    Repository for managing student records.
    """

    def __init__(self, db: DB):
        super().__init__(db, "students")
        self.mappings = {
            "id": "students.id",
            "name": "students.name",
            "advised_by_lecturer_id": "students.advised_by_lecturer_id",
            "date_of_birth": "students.date_of_birth",
            "contact_info": "students.contact_info",
            "program_id": "students.program_id",
            "year_of_study": "students.year_of_study",
            "graduation_status": "students.graduation_status",
            "disciplinary_records": "GROUP_CONCAT(students.disciplinary_records) as disciplinary_records",
            "avg_grade": "AVG(student_enrollments.grade) as avg_grade",
        }

    def map_fields(self, fields):
        return [self.mappings[field] for field in fields if field in self.mappings]

    def map_filters(self, filters):
        return {self.mappings[key]: value for key, value in filters.items()}

    def get_joins(self):
        return """
            LEFT JOIN student_enrollments ON students.id = student_enrollments.student_id
            LEFT JOIN lecturers on students.advised_by_lecturer_id = lecturers.id
            LEFT JOIN courses ON student_enrollments.course_id = courses.id
            LEFT JOIN disciplinary_records on disciplinary_records.student_id = students.id
        """
