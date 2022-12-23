from src.domain.students import Students
from src.repository.student_repository import StudentRepository
from src.services.grades_services import GradeService
from mysql.connector.errors import Error as RepositoryError
import statistics
from operator import itemgetter


class StudentServices:
    def __init__(self):
        self._repo = StudentRepository()
        self._grade_service = GradeService()

    def get_data(self):
        return self._repo.get_all()

    def get_student_by_id(self, student_id: int):
        return self._repo[student_id]

    def insert_data(self, new: Students, for_test=False):
        self._repo.insert(new, for_test)

    def update_data(self, student_id: int, new_name: str, for_test=False):
        self._repo.update_name(student_id, new_name, for_test)

    def revert_after_test(self, new_list: list):
        self._repo.revert_after_test(new_list)

    def delete_data(self, student_id: int, for_test=False):
        self._repo.delete(student_id, for_test)
        try:
            if not for_test:
                self._grade_service.delete(student_id, id_type='student')
        except RepositoryError:
            pass

    def search_for_student(self, name: str):
        students = self._repo.get_all()
        found_students = list()
        for student in students:
            if name.upper() in student.name.upper():
                found_students.append(student)

        return found_students

    def get_failing_students(self):
        failing_students = list()
        for student in self._repo:
            try:
                grades_by_discipline = self._grade_service.get_all_grades_of_a_student_by_discipline(student.student_id)
                for grades in grades_by_discipline.values():
                    if statistics.mean(grades) < 5:
                        failing_students.append(student)
                        break
            except RepositoryError:
                pass

        return failing_students

    def sort_students_by_average(self):
        student_list_with_averages = dict()
        for student in self._repo:
            try:
                grades_by_discipline = self._grade_service.get_all_grades_of_a_student_by_discipline(student.student_id)
                average_by_discipline = list()
                for grades in grades_by_discipline.values():
                    average_by_discipline.append(statistics.mean(grades))
                student_average = statistics.mean(average_by_discipline)
                student_list_with_averages[student] = student_average
            except RepositoryError:
                pass

        sorted_list = sorted(student_list_with_averages.items(), key=lambda x: x[1], reverse=True)
        return sorted_list
