from src.domain.disciplines import Disciplines
from src.repository.general_repository import Repository
from mysql.connector.errors import Error as RepositoryError


class DisciplineRepository(Repository):
    """
    Predefined functions
    """
    def __init__(self):
        super().__init__()
        self.__data = self.__load_data()

    def __len__(self):
        return len(self.__data)

    def __iter__(self):
        for discipline in self.__data:
            yield discipline

    def __getitem__(self, discipline_id: int):
        return self.__data[self.__get_index_by_discipline_id(discipline_id)]

    """
    Auxiliary functions
    """

    def __get_index_by_discipline_id(self, discipline_id_to_find: int):
        for i, discipline in enumerate(self.__data):
            if discipline.discipline_id == discipline_id_to_find:
                return i
        raise RepositoryError("ID not found")

    """
    CRUD operations
    """

    # CREATE
    def insert(self, new_discipline: Disciplines, for_test: bool):
        if new_discipline.discipline_id in [discipline.discipline_id for discipline in self.__data]:
            raise RepositoryError("Discipline does not exist")
        self.__data.append(new_discipline)
        self.__insert_data(new_discipline, for_test)

    # READ
    def get_all(self):
        return self.__data

    # UPDATE
    def update_name(self, discipline_id: int, new_name: str, for_test: bool):
        index = self.__get_index_by_discipline_id(discipline_id)
        self.__data[index].name = new_name
        self.__update_data(discipline_id, new_name, for_test)

    def update_all(self, new_list: list):
        self.__data = new_list

    # DELETE
    def delete(self, discipline_id: int, for_test: bool):
        index = self.__get_index_by_discipline_id(discipline_id)
        self.__data.pop(index)
        self.__delete_data(discipline_id, for_test)

    """
    MYSQL database operations
    """
    def __load_data(self):
        self._cursor.execute('SELECT * FROM disciplines')
        extracted_data = list()
        for row in self._cursor:
            discipline_id = row[0]
            discipline_name = row[1]
            extracted_data.append(Disciplines(discipline_id, discipline_name))

        return extracted_data

    def __insert_data(self, new_discipline: Disciplines, for_test: bool):
        self._cursor.execute(
            'INSERT INTO disciplines VALUES (%s, %s)',
            [new_discipline.discipline_id, new_discipline.name]
        )
        if for_test:
            self._database.rollback()
        else:
            self._database.commit()

    def __update_data(self, discipline_id: int, new_name: str, for_test: bool):
        self._cursor.execute(
            """
            UPDATE disciplines
            SET name = (%s)
            WHERE id = (%s)
            """,
            [new_name, discipline_id]
        )
        if for_test:
            self._database.rollback()
        else:
            self._database.commit()

    def __delete_data(self, discipline_id: int, for_test: bool):
        self._cursor.execute(
            """
            DELETE FROM disciplines
            WHERE id=(%s)
            """,
            [discipline_id]
        )
        if for_test:
            self._database.rollback()
        else:
            self._database.commit()