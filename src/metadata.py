"""metadata.py"""
import copy
from data import (
    StudentRepository,
    CourseRepository,
    DepartmentRepository,
    LecturerRepository,
    StaffRepository,
)



class MetadataProvider:
    """A class to extract field names from the data stored in the
    repositories and assign it to a table name"""
    def __init__(
        self,
        student_repo: StudentRepository,
        course_repo: CourseRepository,
        lecturer_repo: LecturerRepository,
        department_repo: DepartmentRepository,
        staff_repo: StaffRepository,
    ):
        self.student_repo = student_repo
        self.course_repo = course_repo
        self.lecturer_repo = lecturer_repo
        self.department_repo = department_repo
        self.staff_repo = staff_repo

        self.table_metadata = [
            {
                "table_name": "students",
                "column_names": student_repo.get_column_names(),
            },
            {
                "table_name": "courses",
                "column_names": course_repo.get_column_names(),
            },
            {
                "table_name": "departments",
                "column_names": department_repo.get_column_names(),
            },
            {
                "table_name": "staff",
                "column_names": staff_repo.get_column_names(),
            },
            {
                "table_name": "lecturers",
                "column_names": lecturer_repo.get_column_names(),
            },
        ]

    def get_table_metadata(self, table_name):
        """Retrieves specific table metadata from list of dictionaries"""
        table_metadata = self.get_all_table_metadata()
        for i in range(0, len(table_metadata)):
            if table_metadata[i].get("table_name") == table_name:
                return table_metadata[i]
        return None

    def get_all_table_metadata(self):
        """Retrieves all table metadata"""
        return copy.deepcopy(self.table_metadata)
