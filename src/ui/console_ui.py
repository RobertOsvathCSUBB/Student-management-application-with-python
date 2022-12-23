from src.domain.students import Students
from src.domain.disciplines import Disciplines
from src.domain.grades import Grades
from src.services.disciplines_services import DisciplineServices
from src.services.students_services import StudentServices
from src.services.grades_services import GradeService
from texttable import Texttable


class ConsoleUI:
    def __init__(self):
        self._students_service = StudentServices()
        self._disciplines_service = DisciplineServices()
        self._grades_service = GradeService()
        self._menu()

    def update(self):
        self._students_service = StudentServices()
        self._disciplines_service = DisciplineServices()
        self._grades_service = GradeService()

    def _display_databases(self, database: str):
        table = Texttable()
        match database:
            case 'students':
                table.add_row(['Student ID', 'Student name'])
                data = self._students_service.get_data()
                for discipline in data:
                    table.add_row([discipline.student_id, discipline.name])
            case 'disciplines':
                table.add_row(['Discipline ID', 'Discipline name'])
                data = self._disciplines_service.get_data()
                for discipline in data:
                    table.add_row([discipline.discipline_id, discipline.name])

        print(table.draw())

    @staticmethod
    def _display_after_search_or_statistics(display_list: list, database: str):
        table = Texttable()
        match database:
            case 'students':
                table.add_row(['Student ID', 'Student name'])
                data = display_list
                for discipline in data:
                    table.add_row([discipline.student_id, discipline.name])
            case 'disciplines':
                table.add_row(['Discipline ID', 'Discipline name'])
                data = display_list
                for discipline in data:
                    table.add_row([discipline.discipline_id, discipline.name])

        print(table.draw())

    def display_sorted_students(self):
        table = Texttable()
        table.add_row(['Student ID', 'Student name', 'Student average'])
        data = self._students_service.sort_students_by_average()
        for element in data:
            student = element[0]
            average = element[1]
            table.add_row([student.student_id, student.name, average])

        print(table.draw())

    def display_sorted_disciplines(self):
        table = Texttable()
        table.add_row(['Discipline ID', 'Discipline name', 'Discipline average'])
        data = self._disciplines_service.get_all_disciplines_with_at_least_a_grade_per_student()
        for element in data:
            discipline = element[0]
            average = element[1]
            table.add_row([discipline.discipline_id, discipline.name, average])

        print(table.draw())

    def _manage_databases(self):
        print("Select database")
        print("> 1. Students")
        print("> 2. Disciplines")
        select_database_input = int(input("> >"))

        if select_database_input not in [1, 2]:
            raise ValueError("Invalid input")

        print("> > 1. Add")
        print("> > 2. Remove")
        print("> > 3. Update")
        print("> > 4. List")
        select_operation_input = int(input("> > >"))

        match select_operation_input:
            case 1:
                if select_database_input == 1:
                    new_student = Students.create_from_string(input("> > > > New student: "))
                    self._students_service.insert_data(new_student)
                elif select_database_input == 2:
                    new_discipline = Disciplines.create_from_string(input("> > > > New discipline: "))
                    self._disciplines_service.insert_data(new_discipline)
            case 2:
                if select_database_input == 1:
                    student_id_to_delete = int(input("> > > > ID of student: "))
                    self._students_service.delete_data(student_id_to_delete)
                elif select_database_input == 2:
                    discipline_id_to_delete = int(input("> > > > ID of discipline: "))
                    self._disciplines_service.delete_data(discipline_id_to_delete)
            case 3:
                if select_database_input == 1:
                    student_id_to_update = int(input("> > > > ID of student: "))
                    new_name = input("> > > > New name: ")
                    self._students_service.update_data(student_id_to_update, new_name)
                elif select_database_input == 2:
                    discipline_id_to_update = int(input("> > > > ID of discipline: "))
                    new_name = input("> > > > New name: ")
                    self._disciplines_service.update_data(discipline_id_to_update, new_name)
            case 4:
                if select_database_input == 1:
                    self._display_databases("students")
                elif select_database_input == 2:
                    self._display_databases("disciplines")
            case invalid_command:
                raise ValueError("Invalid input")

    def _grade_student(self, new_grade: Grades):
        self._grades_service.insert(new_grade)

    def search_for(self):
        print("> 1. Student")
        print("> 2. Discipline")
        select_search_input = int(input("> > "))

        match select_search_input:
            case 1:
                name = input("> > > Name: ")
                self._display_after_search_or_statistics(self._students_service.search_for_student(name), 'students')
            case 2:
                discipline = input("> > > Discipline: ")
                self._display_after_search_or_statistics(self._disciplines_service.search_for_discipline(discipline),
                                                         'disciplines')
            case invalid_command:
                raise ValueError("invalid input")

    def statistics(self):
        print("> 1. Find out who is failing")
        print("> 2. Sort the students with the best average grades")
        print("> 3. Sort the disciplines by the average grade")
        select_operation_input = int(input("> > "))

        match select_operation_input:
            case 1:
                failing_students = self._students_service.get_failing_students()
                if len(failing_students) == 0:
                    print("There are no students failing")
                else:
                    print("Failing students: ")
                    self._display_after_search_or_statistics(failing_students, 'students')
            case 2:
                self.display_sorted_students()
            case 3:
                self.display_sorted_disciplines()
            case invalid_command:
                raise ValueError("Invalid input")

    def _menu(self):
        while True:
            print("Options: ")
            print("1. Manage databases")
            print("2. Grade a student")
            print("3. Search for a student or a discipline")
            print("4. Statistics")
            print("5. Exit")
            try:
                user_option_input = int(input(">"))
                match user_option_input:
                    case 1:
                        self._manage_databases()
                        self.update()
                    case 2:
                        student_id_to_grade = int(input("> > Choose a student: "))
                        discipline_id = int(input("> > Choose a discipline: "))
                        grade = int(input("> > Grade: "))
                        self._grade_student(Grades(student_id_to_grade, discipline_id, grade))
                        self.update()
                    case 3:
                        self.search_for()
                        self.update()
                    case 4:
                        self.statistics()
                        self.update()
                    case 5:
                        exit()
                    case invalid_command:
                        raise ValueError("Invalid input")
            except Exception as exc:
                print(exc)
