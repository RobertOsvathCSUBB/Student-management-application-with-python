from src.services.grades_services import GradeService
from src.domain.grades import Grades
from src.repository.student_repository import StudentRepository
from src.repository.discipline_repository import DisciplineRepository
from mysql.connector.errors import Error as RepositoryError
import unittest
import random


class TestGradeServices(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._services = GradeService()

    def setUp(self) -> None:
        self._test_before_data = self._services.get_all()

    def tearDown(self) -> None:
        self._services.revert_after_test(self._test_before_data)

    def test_insert(self):
        random_student_id = random.choice([student.student_id for student in StudentRepository()])
        random_discipline_id = random.choice([discipline.discipline_id for discipline in DisciplineRepository()])
        grade = Grades(random_student_id, random_discipline_id, random.randint(0, 10))
        self._services.insert(grade, for_test=True)
        self.assertIn(grade, self._services.get_all(), "Insert not working")

    def test_delete(self):
        random_grade = random.choice(self._services.get_all())
        self._services.delete(random_grade.student_id, 'student', for_test=True)
        self.assertNotIn(random_grade, self._services.get_all(), "Delete not working")

    def test_get_all(self):
        self.assertIsInstance(self._services.get_all(), list, "Get all not working")

    def test_get_all_grades_of_a_student_by_discipline(self):
        while True:
            try:
                random_student_id = random.choice([student.student_id for student in StudentRepository()])
                grades_by_discipline = self._services.get_all_grades_of_a_student_by_discipline(random_student_id)
                for discipline, grades in grades_by_discipline.items():
                    self.assertIn(discipline, [discipline.discipline_id for discipline in DisciplineRepository()],
                                  "Get all grades of a student by discipline not working")
                    self.assertIsInstance(grades, list, "Get all grades of a student by discipline not working")
                break
            except RepositoryError:
                pass

    def test_get_disciplines_with_average_grades(self):
        disciplines_with_grades = self._services.get_disciplines_with_average_grades()
        for discipline, grade in disciplines_with_grades.items():
            self.assertIn(discipline, [discipline.discipline_id for discipline in DisciplineRepository()],
                          "Get disciplines with average grades not working")
            self.assertIsInstance(grade, (float, int), "Get disciplines with average grades not working")
