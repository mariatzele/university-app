from ..db import DB
from .base_repository import BaseRepository


class LecturerRepository(BaseRepository):
    """
    Repository for managing lecturer records.
    """

    def __init__(self, db: DB):
        super().__init__(db, "lecturers")

    def get_joins(self):
        # Important! We need the join to `programs` because we will then get the
        # employees who supervise student employees in a particular program.
        # We get this through: Program -> Student -> Advised By (Lecturer)
        return """
            LEFT JOIN students ON students.advised_by_lecturer_id = lecturers.id
            LEFT JOIN programs on programs.id = students.program_id
            LEFT JOIN research_projects on research_projects.principal_investigator = lecturers.id
        """
