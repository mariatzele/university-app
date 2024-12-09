import unittest
from pprint import pprint
from dotenv import load_dotenv
from src.data import DepartmentRepository, DB, Filter, Operators

load_dotenv()


class TestDepartmentRepository(unittest.TestCase):

    def setUp(self):
        db = DB()
        self.repo = DepartmentRepository(db)

    def test_find_all_staff_members_employed_in_a_specific_department(self):
        """
        Find all staff members employed in a specific department
        """
        filter = Filter()
        filter.add_condition("departments.id", Operators.EQ, 1)

        results = self.repo.search_staff(filter)
        self.assertIsInstance(results, list)
        self.assertGreaterEqual(len(results), 0)

        academic_staff = [r for r in results if r["academic_staff"]]
        non_academic_staff = [r for r in results if not r["academic_staff"]]

        self.assertEqual(len(academic_staff), 2)
        self.assertEqual(len(non_academic_staff), 1)
