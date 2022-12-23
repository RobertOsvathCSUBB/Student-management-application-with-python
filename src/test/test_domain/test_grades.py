from src.domain.grades import Grades
import unittest


class TestGrades(unittest.TestCase):
    def test_initialize(self):
        grade = Grades(1, 1, 10)
        self.assertEqual(grade.discipline_id, 1, "Incorrect discipline id")
        self.assertEqual(grade.student_id, 1, "Incorrect student id")
        self.assertEqual(grade.grade_value, 10, "Incorrect grade value")
