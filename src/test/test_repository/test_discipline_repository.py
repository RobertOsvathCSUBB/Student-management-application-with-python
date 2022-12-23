from src.repository.discipline_repository import DisciplineRepository
from src.domain.disciplines import Disciplines
from mysql.connector.errors import Error as RepositoryError
import unittest
import random


class TestDisciplineRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._repo = DisciplineRepository()

    def test_predefined(self):
        try:
            for _ in self._repo:
                pass
        except TypeError:
            self.assertFalse(True, "Iter not working")
        try:
            self.assertIsInstance(self._repo.__getitem__(random.choice(self._repo).discipline_id), Disciplines, "Getitem not working") # NOQA
        except RepositoryError:
            self.assertTrue(True)

    def test_update_when_exception(self):
        with self.assertRaises(RepositoryError):
            self._repo.update_name(-1, "This is a test", for_test=True)

    def test_delete_when_exception(self):
        with self.assertRaises(RepositoryError):
            self._repo.delete(-1, for_test=True)
