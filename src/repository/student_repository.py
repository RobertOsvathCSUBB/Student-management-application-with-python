from src.domain.students import Students
from src.repository.general_repository import Repository
from mysql.connector.errors import Error as RepositoryError


class StudentRepository(Repository):
    """
    Predefined functions
    """
    def __init__(self):
        super().__init__()
        self.__data = self.__load_data()

    def __len__(self):
        return len(self.__data)

    def __iter__(self):
        for student in self.__data:
            yield student

    def __getitem__(self, student_id: int):
        return self.__data[self.__get_index_by_student_id(student_id)]

    """
    Auxiliary functions
    """

    def __get_index_by_student_id(self, student_id_to_find: int):
        for i, student in enumerate(self.__data):
            if student.student_id == student_id_to_find:
                return i
        raise RepositoryError("Id not found")

    """
    CRUD operations
    """
    # CREATE
    def insert(self, new_student: Students, for_test: bool):
        if new_student.student_id in [student.student_id for student in self.__data]:
            raise RepositoryError("Student already exists")
        self.__data.append(new_student)
        self.__insert_data(new_student, for_test)

    # READ
    def get_all(self):
        return self.__data

    # UPDATE
    def update_name(self, student_id: int, new_name: str, for_test: bool):
        index = self.__get_index_by_student_id(student_id)
        self.__data[index].name = new_name
        self.__update_data(student_id, new_name, for_test)

    def revert_after_test(self, new_list: list):
        self.__data = new_list

    # DELETE
    def delete(self, student_id: int, for_test: bool):
        index = self.__get_index_by_student_id(student_id)
        self.__data.pop(index)
        self.__delete_data(student_id, for_test)
    """
    MYSQL database operations
    """
    def __load_data(self):
        self._cursor.execute('SELECT * FROM students')
        extracted_data = list()
        for row in self._cursor:
            student_id = row[0]
            student_name = row[1]
            extracted_data.append(Students(student_id, student_name))

        return extracted_data

    def __insert_data(self, new_student: Students, for_test: bool):
        self._cursor.execute(
            'INSERT INTO students VALUES (%s, %s)',
            [new_student.student_id, new_student.name]
        )
        if for_test:
            self._database.rollback()
        else:
            self._database.commit()

    def __update_data(self, student_id: int, new_name: str, for_test: bool):
        self._cursor.execute(
            """
            UPDATE students
            SET name = (%s)
            WHERE id = (%s)
            """,
            [new_name, student_id]
        )
        if for_test:
            self._database.rollback()
        else:
            self._database.commit()

    def __delete_data(self, student_id: int, for_test: bool):
        self._cursor.execute(
            """
            DELETE FROM students
            WHERE id=(%s)
            """,
            [student_id]
        )
        if for_test:
            self._database.rollback()
        else:
            self._database.commit()
