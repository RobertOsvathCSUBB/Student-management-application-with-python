from src.domain.grades import Grades
from src.repository.grades_repository import GradesRepository
import statistics


class GradeService:
    def __init__(self):
        self._repo = GradesRepository()

    def insert(self, new_grade: Grades, for_test=False):
        self._repo.insert(new_grade, for_test)

    def delete(self, id: int, id_type: str, for_test=False):
        self._repo.delete(id, id_type, for_test)

    def get_all(self):
        return self._repo.get_all()

    def revert_after_test(self, new_list: list):
        self._repo.revert_after_test(new_list)

    def get_all_grades_of_a_student_by_discipline(self, student_id: int):
        grades_by_discipline = dict()
        for grade_index in self._repo.get_grades(student_id, id_type='student'):
            if self._repo[grade_index].discipline_id not in grades_by_discipline:
                grades_by_discipline[self._repo[grade_index].discipline_id] = [self._repo[grade_index].grade_value]
            else:
                grades_by_discipline[self._repo[grade_index].discipline_id].append(self._repo[grade_index].grade_value) # NOQA PEP8

        return grades_by_discipline

    def get_disciplines_with_average_grades(self):
        disciplines = dict()
        for grade in self._repo:
            if grade.discipline_id not in disciplines:
                disciplines[grade.discipline_id] = [grade.grade_value]
            else:
                disciplines[grade.discipline_id].append(grade.grade_value)

        for discipline, grades in disciplines.items():
            average = statistics.mean(grades)
            disciplines[discipline] = average

        return disciplines
