from gui import App
from dotenv import load_dotenv
from data import (
    DB,
    StudentRepository,
    CourseRepository,
    LecturerRepository,
    DepartmentRepository,
    StaffRepository,
)

load_dotenv()

db = DB()
student_repo = StudentRepository(db)
course_repo = CourseRepository(db)
lecturer_repo = LecturerRepository(db)
department_repo = DepartmentRepository(db)
staff_repo = StaffRepository(db)

app = App(
    student_repo=student_repo,
    course_repo=course_repo,
    lecturer_repo=lecturer_repo,
    department_repo=department_repo,
    staff_repo=staff_repo,
)

app.start()

db.close()
