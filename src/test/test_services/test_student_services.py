from src.domain.students import Students
from src.services.students_services import StudentServices
from mysql.connector.errors import Error as RepositoryError
import unittest
import random
import copy


class TestStudentServices(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._services = StudentServices()

    def setUp(self) -> None:
        self._before_test_data = self._services.get_data()

    def tearDown(self) -> None:
        self._services.revert_after_test(self._before_test_data)

    def test_insert_data(self):
        student = Students.create_from_string(f'{random.randint(200, 300)} This is a test')
        self._services.insert_data(student, for_test=True)
        self.assertIn(student, self._services.get_data(), "Insert not working")

    def test_get_all(self):
        self.assertIsInstance(self._services.get_data(), list, "Get all not working")

    def test_delete_data(self):
        with self.assertRaises(RepositoryError):
            self._services.update_data(-1, "This is a test")

        student = random.choice(self._services.get_data())
        self._services.delete_data(student.student_id, for_test=True)
        self.assertNotIn(student, self._services.get_data(), "Delete not working")

    def test_update_data(self):
        with self.assertRaises(RepositoryError):
            self._services.update_data(-1, "This is a test")

        student_id = copy.copy(random.choice(self._services.get_data()).student_id)
        self._services.update_data(student_id, "This is a test", for_test=True)
        self.assertEqual(self._services.get_student_by_id(student_id).name, "This is a test", "Update not working")

    def test_search_for_student(self):
        random_student = random.choice(self._services.get_data())
        search_list = self._services.search_for_student(random_student.name)
        self.assertIn(random_student, search_list, "Search not working")

    def test_get_failing_students(self):
        failing_students = self._services.get_failing_students()
        for student in failing_students:
            self.assertIsInstance(student, Students, "Failing students not working")

    def test_sort_students_by_average(self):
        sorted_students = self._services.sort_students_by_average()
        self.assertEqual(sorted_students, sorted(sorted_students, key=lambda x: x[1], reverse=True), "Sort not working")
