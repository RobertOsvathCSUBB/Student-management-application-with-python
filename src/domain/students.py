from src.domain.validators import Validators


class Students:
    def __init__(self, student_id: int, name: str):
        Validators.validate_student(student_id)
        self._student_id = student_id
        self._name = name

    @property
    def student_id(self):
        return self._student_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new):
        self._name = new

    @classmethod
    def create_from_string(cls, string: str):
        split_tuple = string.strip().split(maxsplit=1)
        student_id = int(split_tuple[0])
        name = split_tuple[1]

        return cls(student_id, name)
