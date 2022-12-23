from src.domain.disciplines import Disciplines
import unittest


class TestDisciplines(unittest.TestCase):
    def test_initialize(self):
        discipline = Disciplines(1, 'ASC')
        self.assertEqual(discipline.discipline_id, 1, 'Incorrect discipline id')
        self.assertEqual(discipline.name, 'ASC', 'Incorrect discipline name')
