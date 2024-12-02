from gui import App
from dotenv import load_dotenv
from data import DB, StudentRepository

load_dotenv()

db = DB()
student_repo = StudentRepository(db)

app = App(student_repo=student_repo)

app.start()

db.close()
