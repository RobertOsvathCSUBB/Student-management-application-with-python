from src.domain.validators import Validators


class Disciplines:
    def __init__(self, discipline_id: int, name: str):
        Validators.validate_discipline(discipline_id)
        self._discipline_id = discipline_id
        self._name = name

    @property
    def discipline_id(self):
        return self._discipline_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new):
        self._name = new

    @classmethod
    def create_from_string(cls, string: str):
        split_tuple = string.strip().split(maxsplit=1)
        discipline_id = int(split_tuple[0])
        name = split_tuple[1]

        return cls(discipline_id, name)
