from ..db import DB
from ..util import compile_filter


class StudentRepository:
    """
    StudentRepository is responsible for managing student records, which are stored in the MySQL Database.
    It provides methods to create, read, update, and delete (CRUD) records.
    """

    def __init__(self, db: DB):
        self.db = db
        self.table = "students"

    def create(self, student: dict):
        query = f"""
        INSERT INTO {self.table} (
            name,
            advised_by_lecturer_id,
            date_of_birth,
            contact_info,
            program_id,
            year_of_study,
            graduation_status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            student.get("name"),
            student.get("advised_by_lecturer_id"),
            student.get("date_of_birth"),
            student.get("contact_info"),
            student.get("program_id"),
            student.get("year_of_study"),
            student.get("graduation_status"),
        )
        self.db.execute_mutation(query, params)

    def get(self, filter: dict):
        result = self.search(filter)
        return result[0] if result else None

    def update(self, student_id: int, student: dict):
        query = f"""
        UPDATE {self.table} SET 
        name = COALESCE(%s, name),
        advised_by_lecturer_id = COALESCE(%s, advised_by_lecturer_id),
        date_of_birth = COALESCE(%s, date_of_birth),
        contact_info = COALESCE(%s, contact_info),
        program_id = COALESCE(%s, program_id),
        year_of_study = COALESCE(%s, year_of_study),
        graduation_status = COALESCE(%s, graduation_status)
        WHERE id = %s
        """
        # IMPORTANT: use .get here to make sure
        # None is passed correctly (that's like setting to NULL in MySQL)
        params = (
            student.get("name"),
            student.get("advised_by_lecturer_id"),
            student.get("date_of_birth"),
            student.get("contact_info"),
            student.get("program_id"),
            student.get("year_of_study"),
            student.get("graduation_status"),
            student_id,
        )
        self.db.execute_mutation(query, params)

    def delete(self, student_ids: list):
        if len(student_ids) == 0:
            return

        placeholders = ", ".join(["%s"] * len(student_ids))
        query = f"DELETE FROM {self.table} WHERE id IN ({placeholders})"
        self.db.execute_mutation(query, tuple(student_ids))

    def search(self, filter: dict = None):
        """
        Search for students based on the given filter

        :param filter: Dictionary of filters for the search.
        :return: List of students matching the filter criteria.
        """
        if filter:
            where_clause, where_params = compile_filter(filter)
        else:
            where_clause, where_params = "", []

        query = f"SELECT * FROM {self.table}"
        if where_clause:
            query += f" WHERE {where_clause}"

        return self.db.execute_query(query, where_params)
