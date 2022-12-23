import importlib


class Validators:
    @classmethod
    def validate_student(cls, student_id):
        if student_id <= 0:
            raise ValidatorError("ID can't be negative")

        if type(student_id) is not int:
            raise ValidatorError("ID is not valid")

    @classmethod
    def validate_discipline(cls, discipline_id):
        if discipline_id <= 0:
            raise ValidatorError("ID can't be negative")

        if type(discipline_id) is not int:
            raise ValueError("ID not valid")

    @classmethod
    def validate_grade(cls, student_id, discipline_id, grade_value):
        cls.validate_student(student_id)
        cls.validate_discipline(discipline_id)

        student_repo_module = importlib.import_module('src.repository.student_repository')
        discipline_repo_module = importlib.import_module('src.repository.discipline_repository')
        student_repo = getattr(student_repo_module, 'StudentRepository')()
        discipline_repo = getattr(discipline_repo_module, 'DisciplineRepository')()

        if student_id not in [student.student_id for student in student_repo]:
            raise ValidatorError("Student ID not found")
        if discipline_id not in [discipline.discipline_id for discipline in discipline_repo]:
            raise ValidatorError("Discipline ID not found")

        if grade_value not in [i for i in range(11)] or type(grade_value) is not int:
            raise ValidatorError("Grade not valid")


class ValidatorError(Exception):
    pass
