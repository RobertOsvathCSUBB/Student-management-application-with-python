from src.domain.students import Students
import unittest


class TestStudents(unittest.TestCase):
    def test_initialize(self):
        student = Students(1, 'Popescu Anna')
        self.assertEqual(student.student_id, 1, 'Incorrect student id')
        self.assertEqual(student.name, 'Popescu Anna', 'Incorrect student name')
