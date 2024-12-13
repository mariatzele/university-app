# main.py

"""
Initialises and runs the application. Sets up the database connection and
initialises the repositories which are passed to the App class.
"""
from gui import App
from dotenv import load_dotenv
from data import (
    DB,
    StudentRepository,
    CourseRepository,
    LecturerRepository,
    DepartmentRepository,
    StaffRepository,
    ProgramRepository,
)

load_dotenv()

db = DB()
student_repo = StudentRepository(db)
course_repo = CourseRepository(db)
lecturer_repo = LecturerRepository(db)
department_repo = DepartmentRepository(db)
staff_repo = StaffRepository(db)
program_repo = ProgramRepository(db)

app = App(
    student_repo=student_repo,
    course_repo=course_repo,
    lecturer_repo=lecturer_repo,
    department_repo=department_repo,
    staff_repo=staff_repo,
    program_repo=program_repo,
)

app.start()

db.close()
