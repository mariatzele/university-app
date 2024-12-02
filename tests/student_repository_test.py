import unittest
from dotenv import load_dotenv
from mysql.connector import Error
from src.data import StudentRepository, DB
from tests.util import create_database, drop_database, migrate

load_dotenv()


class TestStudentRepository(unittest.TestCase):

    def setUp(self):
        self.db_name = "test_student_repository"
        self.connection = create_database(self.db_name)
        migrate(self.connection)

        db = DB(self.connection)
        self.repo = StudentRepository(db)

    def tearDown(self):
        drop_database(self.db_name, self.connection)

    def test_search_students(self):
        students = self.repo.search(filter={"program_id": [1, 2]})

        print(students)
