import unittest
from pprint import pprint
from dotenv import load_dotenv
from src.data import LecturerRepository, DB, Filter, Operators

load_dotenv()


class TestLecturerRepository(unittest.TestCase):

    def setUp(self):
        db = DB()
        self.repo = LecturerRepository(db)

    def test_retrieve_contact_information_of_advisor_for_student(self):
        """
        Find all Lecturers enrolled in a specific course taught by a particular lecturer.
        """
        filter = Filter()
        filter.add_condition("students.id", Operators.EQ, 1)

        result = self.repo.get(filter)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], 1)

    def test_search_for_lecturers_with_expertise_in_a_particular_research_area(self):
        """
        Search for lecturers with expertise in a particular research area.
        """
        filter = Filter()
        filter.add_condition("expertise", Operators.EQ, "Radioactivity")

        results = self.repo.search(filter)
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)

    def test_identify_lecturers_who_have_supervised_the_most_student_research_project(
        self,
    ):
        """
        Identify lecturers who have supervised the most student research projects.
        """
        results = self.repo.search(
            filter=None,
            fields=["lecturers.*", "COUNT(research_projects.id) as projects_count"],
            limit=3,  # top 3 lecturers with most projects
            orderBy="projects_count DESC",
        )
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 3)

    def test_identify_employees_who_supervise_student_employees_in_a_particular_program(
        self,
    ):
        """
        Identify employees who supervise student employees in a particular program.
        """
        filter = Filter()
        # there's a deep join from lecturer to program so we can do this
        filter.add_condition("programs.id", Operators.EQ, 2)

        results = self.repo.search(filter)
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)
