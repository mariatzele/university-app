"""
lecturer_repository.py
Module for managing lecturer records.
"""
from ..db import DB
from .base_repository import BaseRepository


class LecturerRepository(BaseRepository):
    """
    Repository for managing lecturer records.
    """

    def __init__(self, db: DB):
        super().__init__(db, "lecturers")

    def get_field_mappings(self):
        """
        returns a dictionary that maps human-readable field names to SQL
        database fields
        """
        mappings = {
            "ID": "lecturers.id",
            "Name": "lecturers.name",
            "Qualifications": "lecturers.academic_qualifications",
            "Department": "departments.name",
            "Expertise": "lecturers.expertise",
            "Interests": "lecturers.research_interests",
            "Projects Supervised": "COUNT(research_projects.id)",
            "Programs": "GROUP_CONCAT(programs.name)",
        }
        return mappings

    def get_filter_mappings(self):
        """
        returns a dictionary that maps filter values to SQL
        database fields
        """
        mappings = {
            "id": "lecturers.id",
            "name": "lecturers.name",
            "academic_qualifications": "lecturers.academic_qualifications",
            "department_id": "lecturers.department_id",
            "expertise": "lecturers.expertise",
            "student_id": "students.id",
            "program_id": "programs.id",
            "research_interests": "lecturers.research_interests",
        }
        return mappings

    def get_joins(self):
        """Returns string containing SQL JOIN statements allowing the
        application to make database queries"""
        return """
            LEFT JOIN students ON students.advised_by_lecturer_id = lecturers.id
            LEFT JOIN departments ON departments.id = lecturers.department_id
            LEFT JOIN programs on programs.id = students.program_id
            LEFT JOIN research_projects on research_projects.principal_investigator = lecturers.id
        """