import tkinter as tk
from src.services.students_services import StudentServices
from src.services.disciplines_services import DisciplineServices
from src.services.grades_services import GradeService
from src.domain.students import Students
from src.domain.disciplines import Disciplines
from src.domain.grades import Grades
from texttable import Texttable


class GraphicalUI:
    def __init__(self):
        self.student_service = StudentServices()
        self.discipline_service = DisciplineServices()
        self.grade_service = GradeService()

        self.root = tk.Tk()
        self.root.geometry('500x500')
        self.root.title('Student manager application')
        self.main_page().pack()
        self.root.mainloop()

    def main_page(self):
        main_page_frame = tk.Frame(self.root)

        manage_database_button = tk.Button(main_page_frame, text='Manage databases',
                                           command=lambda: [main_page_frame.pack_forget(),
                                                            self.select_database().pack()])
        manage_database_button.pack(padx=10, pady=10)

        grade_student_button = tk.Button(main_page_frame, text='Grade a student',
                                         command=lambda: [main_page_frame.pack_forget(),
                                                          self.grade_student().pack()])
        grade_student_button.pack(padx=10, pady=10)

        search_button = tk.Button(main_page_frame, text='Search for a student or a database',
                                  command=lambda: [main_page_frame.pack_forget(),
                                                   self.select_database_for_search().pack()])
        search_button.pack(padx=10, pady=10)

        statistics_button = tk.Button(main_page_frame, text='Show statistics',
                                      command=lambda: [main_page_frame.pack_forget(),
                                                       self.statistics().pack()])
        statistics_button.pack(padx=10, pady=10)

        return main_page_frame

    def select_database(self):
        select_databases_frame = tk.Frame(self.root)

        manage_students_button = tk.Button(select_databases_frame, text='Manage students',
                                           command=lambda: [select_databases_frame.pack_forget(),
                                                            self.manage_database('student').pack()])
        manage_students_button.pack(padx=10, pady=10)

        manage_disciplines_button = tk.Button(select_databases_frame, text='Manage disciplines',
                                              command=lambda: [select_databases_frame.pack_forget(),
                                                               self.manage_database('discipline').pack()])
        manage_disciplines_button.pack(padx=10, pady=10)

        back_button = tk.Button(select_databases_frame, text="Back",
                                command=lambda: [select_databases_frame.pack_forget(), self.main_page().pack()])
        back_button.pack(padx=10, pady=10, side="bottom", anchor="center")

        return select_databases_frame

    def manage_database(self, database: str):
        manage_database_frame = tk.Frame(self.root)

        add_button = tk.Button(manage_database_frame, text='Add',
                               command=lambda: [manage_database_frame.pack_forget(),
                                                self.add(database).pack()])
        add_button.pack(padx=10, pady=10)

        remove_button = tk.Button(manage_database_frame, text='Remove',
                                  command=lambda: [manage_database_frame.pack_forget(),
                                                   self.remove(database).pack()])
        remove_button.pack(padx=10, pady=10)

        update_button = tk.Button(manage_database_frame, text='Update',
                                  command=lambda: [manage_database_frame.pack_forget(),
                                                   self.update(database).pack()])
        update_button.pack(padx=10, pady=10)

        list_button = tk.Button(manage_database_frame, text='List',
                                command=lambda: [manage_database_frame.pack_forget(),
                                                 self.list(database).pack()])
        list_button.pack(padx=10, pady=10)

        back_button = tk.Button(manage_database_frame, text="Back",
                                command=lambda: [manage_database_frame.pack_forget(), self.select_database().pack()])
        back_button.pack(padx=10, pady=10, side="bottom", anchor="center")

        return manage_database_frame

    def add(self, database: str):
        add_frame = tk.Frame(self.root)

        match database:
            case 'student':
                add_label = tk.Label(add_frame, text='Add a student')
                add_label.pack()

                add_entry = tk.Entry(add_frame)
                add_entry.bind("<Return>",
                               lambda event: [
                                   self.student_service.insert_data(Students.create_from_string(add_entry.get())),
                                   # NOQA PEP8
                                   add_entry.delete(0, 'end')])
                add_entry.pack()
            case 'discipline':
                add_label = tk.Label(add_frame, text='Add a discipline')
                add_label.pack()

                add_entry = tk.Entry(add_frame)
                add_entry.bind("<Return>",
                               lambda event: [
                                   self.discipline_service.insert_data(Disciplines.create_from_string(add_entry.get())),
                                   # NOQA PEP8
                                   add_entry.delete(0, 'end')])
                add_entry.pack()

        back_button = tk.Button(add_frame, text="Back", command=lambda: [add_frame.pack_forget(), self.manage_database(
            database).pack()])  # NOQA PEP8
        back_button.pack(padx=10, pady=10, side="bottom", anchor="center")

        return add_frame

    def remove(self, database: str):
        remove_frame = tk.Frame(self.root)

        match database:
            case 'student':
                remove_label = tk.Label(remove_frame, text="Remove a student")
                remove_label.pack()

                remove_entry = tk.Entry(remove_frame)
                remove_entry.bind("<Return>",
                                  lambda event: [self.student_service.delete_data(int(remove_entry.get())),
                                                 remove_entry.delete(0, 'end')])
                remove_entry.pack()
            case 'discipline':
                remove_label = tk.Label(remove_frame, text="Remove a discipline")
                remove_label.pack()

                remove_entry = tk.Entry(remove_frame)
                remove_entry.bind("<Return>",
                                  lambda event: [self.discipline_service.delete_data(int(remove_entry.get())),
                                                 remove_entry.delete(0, 'end')])
                remove_entry.pack()

        back_button = tk.Button(remove_frame, text="Back", command=lambda: [remove_frame.pack_forget(),
                                                                            self.manage_database(
                                                                                database).pack()])  # NOQA PEP8
        back_button.pack(padx=10, pady=10, side="bottom", anchor="center")

        return remove_frame

    def update(self, database: str):
        update_frame = tk.Frame(self.root)

        match database:
            case 'student':
                update_label = tk.Label(update_frame, text="Update a student")
                update_label.pack(padx=10, pady=10)

                get_student_id_label = tk.Label(update_frame, text="Input student id:")
                get_student_id_label.pack()

                id_entry = tk.Entry(update_frame)
                id_entry.pack(padx=10, pady=10)

                get_name_label = tk.Label(update_frame, text="Input new name:")
                get_name_label.pack()

                name_entry = tk.Entry(update_frame)
                name_entry.pack()

                update_button = tk.Button(update_frame, text="Update",
                                          command=lambda: [self.student_service.update_data(
                                              int(id_entry.get()),
                                              name_entry.get()
                                          ),
                                              id_entry.delete(0, 'end'), name_entry.delete(0, 'end')])
                update_button.pack(padx=10, pady=10)
            case 'discipline':
                update_label = tk.Label(update_frame, text="Update a discipline")
                update_label.pack(padx=10, pady=10)

                get_student_id_label = tk.Label(update_frame, text="Input discipline id:")
                get_student_id_label.pack(padx=10, pady=10)

                id_entry = tk.Entry(update_frame)
                id_entry.pack(padx=10, pady=10)

                get_name_label = tk.Label(update_frame, text="Input new name:")
                get_name_label.pack()

                name_entry = tk.Entry(update_frame)
                name_entry.pack()

                update_button = tk.Button(update_frame, text="Update",
                                          command=lambda: [self.discipline_service.update_data(int(id_entry.get()),
                                                                                               name_entry.get()),
                                                           # NOQA PEP8
                                                           id_entry.delete(0, 'end'), name_entry.delete(0, 'end')])
                update_button.pack(padx=10, pady=10)

        back_button = tk.Button(update_frame, text="Back", command=lambda: [update_frame.pack_forget(),
                                                                            self.manage_database(
                                                                                database).pack()])  # NOQA PEP8
        back_button.pack(padx=10, pady=10, side="bottom", anchor="center")

        return update_frame

    def list(self, database: str):
        list_frame = tk.Frame(self.root)
        table = Texttable()

        match database:
            case 'student':
                table.add_row(["Student ID", "Student name"])
                data = self.student_service.get_data()
                for student in data:
                    table.add_row([student.student_id, student.name])
            case 'discipline':
                table.add_row(["Discipline ID", "Discipline name"])
                data = self.discipline_service.get_data()
                for discipline in data:
                    table.add_row([discipline.discipline_id, discipline.name])

        table_label = tk.Label(list_frame, text=table.draw())
        table_label.pack()

        back_button = tk.Button(list_frame, text="Back",
                                command=lambda: [list_frame.pack_forget(), self.manage_database(database).pack()])
        back_button.pack(padx=10, pady=10, side="bottom", anchor="center")

        return list_frame

    def grade_student(self):
        grade_frame = tk.Frame(self.root)

        grade_label = tk.Label(grade_frame, text="Grade a student")
        grade_label.pack(padx=10, pady=10)

        student_id_label = tk.Label(grade_frame, text="Student ID:")
        student_id_label.pack()

        student_id_entry = tk.Entry(grade_frame)
        student_id_entry.pack(padx=10, pady=10)

        discipline_id_label = tk.Label(grade_frame, text="Discipline ID:")
        discipline_id_label.pack()

        discipline_id_entry = tk.Entry(grade_frame)
        discipline_id_entry.pack(padx=10, pady=10)

        grade_value_label = tk.Label(grade_frame, text="Grade value:")
        grade_value_label.pack()

        grade_value_entry = tk.Entry(grade_frame)
        grade_value_entry.pack(padx=10, pady=10)

        grade_button = tk.Button(grade_frame, text="Grade",
                                 command=lambda: [self.grade_service.insert(Grades(int(student_id_entry.get()),
                                                                                   int(discipline_id_entry.get()),
                                                                                   int(grade_value_entry.get()))),
                                                  student_id_entry.delete(0, 'end'),
                                                  discipline_id_entry.delete(0, 'end'),
                                                  grade_value_entry.delete(0, 'end')])
        grade_button.pack()

        back_button = tk.Button(grade_frame, text="Back", command=lambda: [grade_frame.pack_forget(),
                                                                           self.main_page().pack()])
        back_button.pack(padx=10, pady=10, side="bottom", anchor="center")

        return grade_frame

    def select_database_for_search(self):
        select_frame = tk.Frame(self.root)

        select_students = tk.Button(select_frame, text='Search for student',
                                    command=lambda: [select_frame.pack_forget(),
                                                     self.search('student').pack()])
        select_students.pack(padx=10, pady=10)

        select_disciplines = tk.Button(select_frame, text='Search for a discipline',
                                       command=lambda: [select_frame.pack_forget(),
                                                        self.search('discipline').pack()])
        select_disciplines.pack(padx=10, pady=10)

        back_button = tk.Button(select_frame, text="Back",
                                command=lambda: [select_frame.pack_forget(), self.main_page().pack()])
        back_button.pack(padx=10, pady=10, side="bottom", anchor="center")

        return select_frame

    def search(self, database: str):
        search_frame = tk.Frame(self.root)

        search_label = tk.Label(search_frame, text="Search:")
        search_label.pack(padx=10, pady=10)

        search_entry = tk.Entry(search_frame)
        search_entry.bind("<Return>", lambda event: self.display_search(search_frame, search_entry.get(), database))
        search_entry.pack()

        back_button = tk.Button(search_frame, text="Back", command=lambda: [search_frame.pack_forget(),
                                                                            self.select_database_for_search().pack()])
        back_button.pack(padx=10, pady=10, side="bottom", anchor="center")

        return search_frame

    def display_search(self, search_frame: tk.Frame, name: str, database: str):
        table = Texttable()

        match database:
            case 'student':
                table.add_row(['Student ID', 'Student name'])
                data = self.student_service.search_for_student(name)
                for student in data:
                    table.add_row([student.student_id, student.name])
            case 'discipline':
                table.add_row(['Discipline ID', 'Discipline name'])
                data = self.discipline_service.search_for_discipline(name)
                for discipline in data:
                    table.add_row([discipline.discipline_id, discipline.name])

        table_label = tk.Label(search_frame, text=table.draw())
        table_label.pack(padx=10, pady=10)

    def statistics(self):
        statistics_frame = tk.Frame(self.root)

        failing_students_button = tk.Button(statistics_frame, text="Get failing students",
                                            command=lambda: [statistics_frame.pack_forget(),
                                                             self.get_failing_students().pack()])
        failing_students_button.pack(padx=10, pady=10)

        sorted_students_button = tk.Button(statistics_frame, text="Get students sorted by average grades",
                                           command=lambda: [statistics_frame.pack_forget(),
                                                            self.sort_students_by_average_grade().pack()])
        sorted_students_button.pack(padx=10, pady=10)

        discipline_averages_button = tk.Button(statistics_frame, text="Get average grades for disciplines",
                                               command=lambda: [statistics_frame.pack_forget(),
                                                                self.sort_disciplines_by_average_grade().pack()])
        discipline_averages_button.pack(padx=10, pady=10)

        back_button = tk.Button(statistics_frame, text="Back", command=lambda: [statistics_frame.pack_forget(),
                                                                                self.main_page().pack()])
        back_button.pack(padx=10, pady=10, side="bottom", anchor="center")

        return statistics_frame

    def get_failing_students(self):
        failing_students_frame = tk.Frame(self.root)

        table = Texttable()
        table.add_row(['Student ID', 'Student name'])
        data = self.student_service.get_failing_students()
        for student in data:
            table.add_row([student.student_id, student.name])

        table_label = tk.Label(failing_students_frame, text=table.draw())
        table_label.pack(padx=10, pady=10)

        back_button = tk.Button(failing_students_frame, text="Back",
                                command=lambda: [failing_students_frame.pack_forget(),
                                                 self.statistics().pack()])
        back_button.pack(padx=10, pady=10, side="bottom", anchor="center")

        return failing_students_frame

    def sort_students_by_average_grade(self):
        sorted_students_frame = tk.Frame(self.root)

        table = Texttable()
        table.add_row(['Student ID', 'Student name', 'Student average'])
        data = self.student_service.sort_students_by_average()
        for element in data:
            student = element[0]
            average = element[1]
            table.add_row([student.student_id, student.name, average])

        table_label = tk.Label(sorted_students_frame, text=table.draw())
        table_label.pack()

        back_button = tk.Button(sorted_students_frame, text="Back",
                                command=lambda: [sorted_students_frame.pack_forget(),
                                                 self.statistics().pack()])
        back_button.pack(padx=10, pady=10, side="bottom", anchor="center")

        return sorted_students_frame

    def sort_disciplines_by_average_grade(self):
        sorted_disciplines_frame = tk.Frame(self.root)

        table = Texttable()
        table.add_row(['Discipline ID', 'Discipline name', 'Discipline average'])
        data = self.discipline_service.get_all_disciplines_with_at_least_a_grade_per_student()
        for element in data:
            discipline = element[0]
            average = element[1]
            table.add_row([discipline.discipline_id, discipline.name, average])

        table_label = tk.Label(sorted_disciplines_frame, text=table.draw())
        table_label.pack()

        back_button = tk.Button(sorted_disciplines_frame, text="Back",
                                command=lambda: [sorted_disciplines_frame.pack_forget(),
                                                 self.statistics().pack()])
        back_button.pack(padx=10, pady=10, side="bottom", anchor="center")

        return sorted_disciplines_frame
