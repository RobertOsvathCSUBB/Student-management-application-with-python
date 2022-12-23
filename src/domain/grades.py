from src.domain.validators import Validators


class Grades:
    def __init__(self, student_id, discipline_id, grade_value):
        Validators.validate_grade(student_id, discipline_id, grade_value)
        self._student_id = student_id
        self._discipline_id = discipline_id
        self._grade_value = grade_value

    @property
    def discipline_id(self):
        return self._discipline_id

    @property
    def student_id(self):
        return self._student_id

    @property
    def grade_value(self):
        return self._grade_value

    @grade_value.setter
    def grade_value(self, new):
        self._grade_value = new

    @classmethod
    def create_from_string(cls, string: str):
        split_tuple = string.split(maxsplit=2)
        student_id = split_tuple[0]
        discipline_id = split_tuple[1]
        grade_value = split_tuple[2]
        return cls(student_id, discipline_id, grade_value)
