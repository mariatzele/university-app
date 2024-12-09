import unittest
from pprint import pprint
from dotenv import load_dotenv
from src.data import CourseRepository, DB, Filter, Operators

load_dotenv()


class TestCourseRepository(unittest.TestCase):

    def setUp(self):
        db = DB()
        self.repo = CourseRepository(db)

    def test_list_all_courses_taught_by_lecturers_in_a_specific_department(self):
        """
        List all courses taught by lecturers in a specific department.
        """
        filter = Filter()
        filter.add_condition("lecturers.department_id", Operators.EQ, 1)

        results = self.repo.search(filter)
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)
