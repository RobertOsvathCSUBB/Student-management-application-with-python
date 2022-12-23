from src.domain.grades import Grades
from src.repository.general_repository import Repository
from mysql.connector.errors import Error as RepositoryError


class GradesRepository(Repository):
    """
    Predefined functions
    """

    def __init__(self):
        super().__init__()
        self.__data = self.__load_data()

    def __iter__(self):
        for grade in self.__data:
            yield grade

    def __getitem__(self, index: int):
        return self.__data[index]

    """
    CRUD operations
    """

    def insert(self, new_grade: Grades, for_test: bool):
        self.__data.append(new_grade)
        self.__insert_data(new_grade, for_test)

    def get_grades(self, id: int, id_type: str):
        grades_list_index = list()
        match id_type:
            case 'student':
                if id not in [grade.student_id for grade in self.__data]:
                    raise RepositoryError("Grade not found")
                for i, grade in enumerate(self.__data):
                    if grade.student_id == id:
                        grades_list_index.append(i)
            case 'discipline':
                if id not in [grade.discipline_id for grade in self.__data]:
                    raise RepositoryError("Grade not found")
                for i, grade in enumerate(self.__data):
                    if grade.discipline_id == id:
                        grades_list_index.append(i)

        return grades_list_index

    def delete(self, id: int, id_type: str, for_test: bool):
        grades_indexes = self.get_grades(id, id_type)
        i = 0
        for to_delete in grades_indexes:
            self.__data.pop(to_delete - i)
            i += 1
        self.__delete_data(id, id_type, for_test)

    def revert_after_test(self, new_list: list):
        self.__data = new_list

    def get_all(self):
        return self.__data

    """
    MYSQL database operations
    """

    def __load_data(self):
        self._cursor.execute('SELECT * FROM grades')
        extracted_data = list()
        for row in self._cursor:
            student_id = row[0]
            discipline_id = row[1]
            grade_value = row[2]
            extracted_data.append(Grades(student_id, discipline_id, grade_value))

        return extracted_data

    def __insert_data(self, new_grade: Grades, for_test: bool):
        self._cursor.execute(
            'INSERT INTO grades VALUES (%s, %s, %s)',
            [new_grade.student_id, new_grade.discipline_id, new_grade.grade_value]
        )
        if for_test:
            self._database.rollback()
        else:
            self._database.commit()

    def __delete_data(self, id: int, id_type: str, for_test: bool):
        match id_type:
            case 'student':
                self._cursor.execute(
                    """
                    DELETE FROM grades
                    WHERE student_id=(%s)
                    """,
                    [id]
                )
            case 'discipline':
                self._cursor.execute(
                    """
                    DELETE FROM grades
                    WHERE student_id=(%s)
                    """,
                    [id]
                )

        if for_test:
            self._database.rollback()
        else:
            self._database.commit()
