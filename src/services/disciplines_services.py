from src.domain.disciplines import Disciplines
from src.repository.discipline_repository import DisciplineRepository
from src.services.grades_services import GradeService
from mysql.connector.errors import Error as RepositoryError


class DisciplineServices:
    def __init__(self):
        self._repo = DisciplineRepository()
        self._grade_service = GradeService()

    def get_data(self):
        return self._repo.get_all()

    def get_discipline_by_id(self, discipline_id: int):
        return self._repo[discipline_id]

    def insert_data(self, new: Disciplines, for_test=False):
        self._repo.insert(new, for_test)

    def update_data(self, discipline_id, new_name, for_test=False):
        self._repo.update_name(discipline_id, new_name, for_test)

    def revert_after_test(self, new_list: list):
        self._repo.update_all(new_list)

    def delete_data(self, discipline_id: int, for_test=False):
        self._repo.delete(discipline_id, for_test)
        try:
            if not for_test:
                self._grade_service.delete(discipline_id, id_type='discipline')
        except RepositoryError:
            pass

    def search_for_discipline(self, name: str):
        discipline = self._repo.get_all()
        found_disciplines = list()
        for discipline in discipline:
            if name.upper() in discipline.name.upper():
                found_disciplines.append(discipline)

        return found_disciplines

    def get_all_disciplines_with_at_least_a_grade_per_student(self):
        disciplines_with_average = dict()
        for discipline_id, average in self._grade_service.get_disciplines_with_average_grades().items():
            disciplines_with_average[self._repo[discipline_id]] = average
        sorted_list = sorted(disciplines_with_average.items(), key=lambda x: x[1], reverse=True)
        return sorted_list
