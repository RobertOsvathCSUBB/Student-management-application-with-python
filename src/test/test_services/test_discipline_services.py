from src.domain.disciplines import Disciplines
from src.services.disciplines_services import DisciplineServices
from mysql.connector.errors import Error as RepositoryError
import unittest
import random
import copy


class TestDisciplineServices(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._services = DisciplineServices()

    def setUp(self) -> None:
        self._before_test_data = self._services.get_data()

    def tearDown(self) -> None:
        self._services.revert_after_test(self._before_test_data)

    def test_insert_data(self):
        discipline = Disciplines.create_from_string(f'{random.randint(200, 300)} This is a test')
        self._services.insert_data(discipline, for_test=True)
        self.assertIn(discipline, self._services.get_data(), "Insert not working")

    def test_get_all(self):
        self.assertIsInstance(self._services.get_data(), list, "Get all not working")

    def test_delete_data(self):
        with self.assertRaises(RepositoryError):
            self._services.update_data(-1, "This is a test")

        discipline = random.choice(self._services.get_data())
        self._services.delete_data(discipline.discipline_id, for_test=True)
        self.assertNotIn(discipline, self._services.get_data(), "Delete not working")

    def test_update_data(self):
        with self.assertRaises(RepositoryError):
            self._services.update_data(-1, "This is a test")

        discipline_id = copy.copy(random.choice(self._services.get_data()).discipline_id)
        self._services.update_data(discipline_id, "This is a test", for_test=True)
        self.assertEqual(self._services.get_discipline_by_id(discipline_id).name, "This is a test", "Update not working")

    def test_search_for_discipline(self):
        random_discipline = random.choice(self._services.get_data())
        search_list = self._services.search_for_discipline(random_discipline.name)
        self.assertIn(random_discipline, search_list, "Search not working")

    def test_get_all_disciplines_with_at_least_a_grade_per_student(self):
        sorted_disciplines = self._services.get_all_disciplines_with_at_least_a_grade_per_student()
        self.assertEqual(sorted_disciplines, sorted(sorted_disciplines, key=lambda x: x[1], reverse=True), "Sort not working")
