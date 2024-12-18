"""
student_repository.py
Module for managing student records.
"""
from ..db import DB
from .base_repository import BaseRepository


class StudentRepository(BaseRepository):
    """
    Repository for managing student records.
    """

    def __init__(self, db: DB):
        super().__init__(db, "students")

    def get_field_mappings(self):
        """
        returns a dictionary that maps human-readable field names to SQL
        database fields
        """
        mappings = {
            "ID": "students.id",
            "Name": "students.name",
            "Advised by": "lecturers.name",
            "Date of birth": "students.date_of_birth",
            "Contact": "students.contact_info",
            "Program": "programs.name",
            "Year of study": "students.year_of_study",
            "Graduated": f"{self.field_to_boolean('students.graduation_status', 'YES', 'NO')}",
            "Disciplinary records": "GROUP_CONCAT(disciplinary_records.description)",
            "Courses": "GROUP_CONCAT(courses.name)",
            "Average grade": "ROUND(AVG(student_enrollments.grade))",
        }
        return mappings

    def get_filter_mappings(self):
        """
        returns a dictionary that maps filter values to SQL
        database fields
        """
        mappings = {
            "id": "students.id",
            "name": "students.name",
            "advised_by_lecturer_id": "students.advised_by_lecturer_id",
            "date_of_birth": "students.date_of_birth",
            "contact_info": "students.contact_info",
            "course_id": "courses.id",
            "program_id": "students.program_id",
            "year_of_study": "students.year_of_study",
            "graduation_status": "students.graduation_status",
            "disciplinary_records": "GROUP_CONCAT(disciplinary_records.description) as disciplinary_records",
            "avg_grade": "ROUND(AVG(student_enrollments.grade)) as avg_grade",
        }
        return mappings

    def get_joins(self):
        """Returns string containing SQL JOIN statements allowing the
        application to make database queries"""
        return """
            LEFT JOIN student_enrollments ON students.id = student_enrollments.student_id
            LEFT JOIN programs on students.program_id = programs.id
            LEFT JOIN lecturers on students.advised_by_lecturer_id = lecturers.id
            LEFT JOIN courses ON student_enrollments.course_id = courses.id
            LEFT JOIN disciplinary_records on disciplinary_records.student_id = students.id
        """
