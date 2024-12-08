import unittest
from pprint import pprint
from dotenv import load_dotenv
from src.data import StudentRepository, DB, Filter, Operators

load_dotenv()


class TestStudentRepository(unittest.TestCase):

    def setUp(self):
        db = DB()
        self.repo = StudentRepository(db)

    def test_find_all_students_enrolled_in_course(self):
        """
        Find all students enrolled in a specific course taught by a particular lecturer.
        """
        filter = Filter()
        filter.add_condition("courses.lecturer_id", Operators.EQ, 1)
        filter.add_condition("courses.id", Operators.EQ, 1)

        results = self.repo.search(filter)
        self.assertIsInstance(results, list)
        self.assertGreaterEqual(len(results), 0)

    def test_students_with_average_grade_above_70_in_final_year(self):
        """
        List all students with an average grade above 70% who are in their final year of studies.
        """
        filter = Filter()
        filter.add_condition("students.year_of_study", Operators.EQ, 4)  # Final year
        filter.add_aggregate_condition(
            "student_enrollments.grade", "AVG", Operators.GT, 70
        )

        results = self.repo.search(
            filter, ["students.*", "AVG(student_enrollments.grade) as avg_grade"]
        )
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], 1)

    def test_students_not_enrolled_in_courses_current_semester(self):
        """
        Identify students who haven't registered for any courses in the current semester.
        """
        filter = Filter()
        filter.add_condition("student_enrollments.student_id", Operators.EQ, None)

        results = self.repo.search(filter)
        self.assertIsInstance(results, list)
        self.assertGreaterEqual(len(results), 0)

    def test_retrieve_the_names_of_students_advised_by_a_specific_lecturer(self):
        """
        Retrieve the names of students advised by a specific lecturer
        """
        filter = Filter()
        filter.add_condition("lecturers.id", Operators.EQ, 1)

        results = self.repo.search(filter, fields=["students.name"])
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 3)
