from src.repository.student_repository import StudentRepository
from src.domain.students import Students
from mysql.connector.errors import Error as RepositoryError
import unittest
import random


class TestStudentRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._repo = StudentRepository()

    def test_predefined(self):
        try:
            for _ in self._repo:
                pass
        except TypeError:
            self.assertFalse(True, "Iter not working")
        try:
            self.assertIsInstance(self._repo.__getitem__(random.choice(self._repo).student_id), Students, "Getitem not working") # NOQA
        except RepositoryError:
            self.assertTrue(True)

    def test_update_when_exception(self):
        with self.assertRaises(RepositoryError):
            self._repo.update_name(-1, "This is a test", for_test=True)

    def test_delete_when_exception(self):
        with self.assertRaises(RepositoryError):
            self._repo.delete(-1, for_test=True)
