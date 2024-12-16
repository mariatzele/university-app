"""
A module for applying filters to various data tables.
"""
import tkinter as tk
from tktooltip import ToolTip
from data import Operators
from data import (
    StudentRepository,
    CourseRepository,
    DepartmentRepository,
    LecturerRepository,
    StaffRepository,
    ProgramRepository,
    Filter,
)


class FilterDialog(tk.Toplevel):
    """
    A dialog window for applying filters to various data tables.
    Allows users to filter data using dynamic criteria.
    """
    def __init__(
        self,
        parent,
        active_table,
        apply_filter_callback,
        student_repo: StudentRepository,
        course_repo: CourseRepository,
        lecturer_repo: LecturerRepository,
        department_repo: DepartmentRepository,
        staff_repo: StaffRepository,
        program_repo: ProgramRepository,
    ):
        self.student_repo = student_repo
        self.course_repo = course_repo
        self.lecturer_repo = lecturer_repo
        self.department_repo = department_repo
        self.staff_repo = staff_repo
        self.program_repo = program_repo

        self.active_table = active_table
        self.apply_filter_callback = apply_filter_callback
        self.filters = {"conditions": {}, "aggregates": {}}

        # load data
        lecturers = self.lecturer_repo.search(
            filter=Filter(), fields=["lecturers.id", "lecturers.name"]
        )
        self.lecturers = [(lecturer["id"], lecturer["name"]) for lecturer in lecturers]

        programs = self.program_repo.search(
            filter=Filter(), fields=["programs.id", "programs.name"]
        )
        self.programs = [(program["id"], program["name"]) for program in programs]

        departments = self.department_repo.search(
            filter=Filter(), fields=["departments.id", "departments.name"]
        )
        self.departments = [
            (department["id"], department["name"]) for department in departments
        ]

        students = self.student_repo.search(
            filter=Filter(), fields=["students.id", "students.name"]
        )
        self.students = [(student["id"], student["name"]) for student in students]

        courses = self.course_repo.search(
            filter=Filter(), fields=["courses.id", "courses.name"]
        )
        self.courses = [(course["id"], course["name"]) for course in courses]
        self.courses.insert(0, ("NULL", "Not enrolled in any course"))

        super().__init__(parent)  # Create a Toplevel window
        self.title("Filter Options")
        self.geometry("450x500")

        # Add widgets to the dialog (example filters)
        tk.Label(self, text="Select Filters:", font=("Arial", 12)).pack(pady=10)

        if active_table == "students":
            self.init_student_filters()
        elif active_table == "courses":
            self.init_course_filters()
        elif active_table == "departments":
            self.init_department_filters()
        elif active_table == "staff":
            self.init_staff_filters()
        elif active_table == "lecturers":
            self.init_lecturer_filters()
        else:
            raise ValueError("invalid table name " + active_table)

        # Add Apply and Cancel buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        apply_button = tk.Button(button_frame, text="Apply", command=self.apply_filters)
        apply_button.pack(side="left", padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=self.destroy)
        cancel_button.pack(side="right", padx=5)

        apply_button.bind("<Return>", lambda event: self.apply_filters())
        cancel_button.bind("<Return>", lambda event: self.destroy())

        ToolTip(widget=apply_button, msg="Load filtered data into "
                                              "table view", delay=1.0)
        ToolTip(widget=cancel_button, msg="Cancel", delay=1.0)

    def apply_filters(self):
        """
        Apply the current filters and close the dialog.
        """
        self.apply_filter_callback(self.filters)
        self.destroy()

    def create_filter(
        self, frame, label_text, var, callback, widget_class=tk.Entry, **widget_options
        ):
        """
        Create a labeled input widget for filter criteria.
        """
        tk.Label(frame, text=label_text).pack(side="left", padx=5)
        widget = widget_class(frame, textvariable=var, **widget_options)
        widget.pack(side="left", padx=5)
        var.trace_add("write", callback)
        return widget


    def create_dropdown(self, parent_frame, data_list, label, callback):
        """
        Create a dropdown menu for selecting filter options.
        """
        # Create the label for the dropdown
        tk.Label(parent_frame, text=label).pack(side="left", padx=5)

        selected_value = tk.StringVar()

        data_dict = {name: data_id for data_id, name in data_list}

        def on_item_selected(*args):
            selected_name = selected_value.get()
            data_id = data_dict.get(selected_name)
            if data_id is not None:
                callback(data_id)

        dropdown = tk.OptionMenu(
            parent_frame,
            selected_value,
            *[name for _, name in data_list],
        )
        dropdown.pack(pady=5)

        selected_value.trace_add("write", on_item_selected)
        selected_value.set(f"Select a {label.lower()}")

        return selected_value

    def init_student_filters(self):
        """
        Initialize and display filters for student data.
        """
        # Name Filter
        name_filter = tk.StringVar()
        name_frame = tk.Frame(self)
        name_frame.pack(pady=10)
        self.create_filter(
            name_frame,
            "Search for name like:",
            name_filter,
            lambda *args: self.filters["conditions"].update(
                {"name": (Operators.LIKE, "%" + name_filter.get() + "%")}
            ),
        )

        # Year of Study Filter
        year_filter = tk.StringVar()
        year_frame = tk.Frame(self)
        year_frame.pack(pady=10)
        self.create_filter(
            year_frame,
            "Year of Study:",
            year_filter,
            lambda *args: self.filters["conditions"].update(
                {"year_of_study": (Operators.EQ, int(year_filter.get()))}
            ),
        )

        # Advised by Lecturer Filter
        lecturer_frame = tk.Frame(self)
        lecturer_frame.pack(pady=10)
        self.create_dropdown(
            lecturer_frame,
            self.lecturers,
            "Advised by",
            lambda lecturer_id: self.filters["conditions"].update(
                {"advised_by_lecturer_id": (Operators.EQ, lecturer_id)}
            ),
        )

        # Enrolled in course
        course_frame = tk.Frame(self)
        course_frame.pack(pady=10)
        self.create_dropdown(
            course_frame,
            self.courses,
            "Enrolled in course",
            lambda course_id: self.filters["conditions"].update(
                {"course_id": (Operators.EQ, course_id)}
            ),
        )

        # Contact Info Filter
        contact_filter = tk.StringVar()
        contact_frame = tk.Frame(self)
        contact_frame.pack(pady=10)
        self.create_filter(
            contact_frame,
            "Contact Info contains:",
            contact_filter,
            lambda *args: self.filters["conditions"].update(
                {"contact_info": (Operators.LIKE, "%" + contact_filter.get() + "%")}
            ),
        )

        # Program Filter
        program_frame = tk.Frame(self)
        program_frame.pack(pady=10)
        self.create_dropdown(
            program_frame,
            self.programs,
            "Program",
            lambda program_id: self.filters["conditions"].update(
                {"program_id": (Operators.EQ, program_id)}
            ),
        )

        # Average grade filter
        avg_grade_filter = tk.StringVar()
        avg_grade_frame = tk.Frame(self)
        avg_grade_frame.pack(pady=10)
        self.create_filter(
            avg_grade_frame,
            "Average grade higher than:",
            avg_grade_filter,
            lambda *args: self.filters["aggregates"].update(
                {
                    # can't use avg_grade here because it's in the SELECT
                    "student_enrollments.grade": (
                        "AVG",
                        Operators.GT,
                        int(avg_grade_filter.get()),
                    )
                }
            ),
        )

        # Graduation Status Filter (Checkbox)
        grad_status_filter = tk.BooleanVar()
        grad_status_frame = tk.Frame(self)
        grad_status_frame.pack(pady=10)
        tk.Label(grad_status_frame, text="Graduation Status:").pack(side="left", padx=5)
        grad_status_checkbox = tk.Checkbutton(
            grad_status_frame,
            text="Graduated",
            variable=grad_status_filter,
            onvalue=True,
            offvalue=False,
            command=lambda: self.filters["conditions"].update(
                {"graduation_status": (Operators.EQ, grad_status_filter.get())}
            ),
        )
        grad_status_checkbox.pack(side="left", padx=5)

    def init_course_filters(self):
        """
        Initialize and display filters for course data.
        """
        # Name Filter
        name_filter = tk.StringVar()
        name_frame = tk.Frame(self)
        name_frame.pack(pady=10)
        self.create_filter(
            name_frame,
            "Search for name like:",
            name_filter,
            lambda *args: self.filters["conditions"].update(
                {"name": (Operators.LIKE, "%" + name_filter.get() + "%")}
            ),
        )

        # Description
        description_filter = tk.StringVar()
        description_frame = tk.Frame(self)
        description_frame.pack(pady=10)
        self.create_filter(
            description_frame,
            "Search for description like:",
            description_filter,
            lambda *args: self.filters["conditions"].update(
                {"description": (Operators.LIKE, "%" + description_filter.get() + "%")}
            ),
        )

        # Lecturer
        lecturer_frame = tk.Frame(self)
        lecturer_frame.pack(pady=10)
        self.create_dropdown(
            lecturer_frame,
            self.lecturers,
            "Lecturer",
            lambda lecturer_id: self.filters["conditions"].update(
                {"lecturer_id": (Operators.EQ, lecturer_id)}
            ),
        )

        # Department
        department_frame = tk.Frame(self)
        department_frame.pack(pady=10)
        self.create_dropdown(
            department_frame,
            self.departments,
            "Department",
            lambda department_id: self.filters["conditions"].update(
                {"department_id": (Operators.EQ, department_id)}
            ),
        )

        # Level
        level_filter = tk.StringVar()
        level_frame = tk.Frame(self)
        level_frame.pack(pady=10)
        self.create_filter(
            level_frame,
            "Level:",
            level_filter,
            lambda *args: self.filters["conditions"].update(
                {"level": (Operators.EQ, int(level_filter.get()))}
            ),
        )

        # Credits
        credits_filter = tk.StringVar()
        credits_frame = tk.Frame(self)
        credits_frame.pack(pady=10)
        self.create_filter(
            credits_frame,
            "Credits:",
            credits_filter,
            lambda *args: self.filters["conditions"].update(
                {"credits": (Operators.EQ, int(credits_filter.get()))}
            ),
        )

    def init_department_filters(self):
        """
        Initialize and display filters for department data.
        """
        # Name Filter
        name_filter = tk.StringVar()
        name_frame = tk.Frame(self)
        name_frame.pack(pady=10)
        self.create_filter(
            name_frame,
            "Search for name like:",
            name_filter,
            lambda *args: self.filters["conditions"].update(
                {"name": (Operators.LIKE, name_filter.get() + "%")}
            ),
        )

        # Research areas
        research_areas_filter = tk.StringVar()
        research_areas_frame = tk.Frame(self)
        research_areas_frame.pack(pady=10)
        self.create_filter(
            research_areas_frame,
            "Search for research areas like:",
            research_areas_filter,
            lambda *args: self.filters["conditions"].update(
                {
                    "research_areas": (
                        Operators.LIKE,
                        "%" + research_areas_filter.get() + "%",
                    )
                }
            ),
        )

    def init_staff_filters(self):
        """
        Initialize and display filters for staff data.
        """
        # Name Filter
        name_filter = tk.StringVar()
        name_frame = tk.Frame(self)
        name_frame.pack(pady=10)
        self.create_filter(
            name_frame,
            "Search for staff name like:",
            name_filter,
            lambda *args: self.filters["conditions"].update(
                {"name": (Operators.LIKE, "%" + name_filter.get() + "%")}
            ),
        )

        # Department
        department_frame = tk.Frame(self)
        department_frame.pack(pady=10)
        self.create_dropdown(
            department_frame,
            self.departments,
            "Department",
            lambda department_id: self.filters["conditions"].update(
                {"department_id": (Operators.EQ, department_id)}
            ),
        )

        # Department name
        department_name_filter = tk.StringVar()
        department_name_frame = tk.Frame(self)
        department_name_frame.pack(pady=10)
        self.create_filter(
            department_name_frame,
            "Search for department name like:",
            department_name_filter,
            lambda *args: self.filters["conditions"].update(
                {
                    "department_name": (
                        Operators.LIKE,
                        "%" + department_name_filter.get() + "%",
                    )
                }
            ),
        )

        # Academic Staff Filter (Checkbox)
        academic_staff_filter = tk.BooleanVar()
        academic_staff_frame = tk.Frame(self)
        academic_staff_frame.pack(pady=10)
        tk.Label(academic_staff_frame, text="Graduation Status:").pack(
            side="left", padx=5
        )
        academic_staff_checkbox = tk.Checkbutton(
            academic_staff_frame,
            text="Academic Staff",
            variable=academic_staff_filter,
            onvalue=True,
            offvalue=False,
            command=lambda: self.filters["conditions"].update(
                {"academic_staff": (Operators.EQ, academic_staff_filter.get())}
            ),
        )
        academic_staff_checkbox.pack(side="left", padx=5)

    def init_lecturer_filters(self):
        """
        Initialize and display filters for lecturer data.
        """
        # Name Filter
        name_filter = tk.StringVar()
        name_frame = tk.Frame(self)
        name_frame.pack(pady=10)
        self.create_filter(
            name_frame,
            "Search for name like:",
            name_filter,
            lambda *args: self.filters["conditions"].update(
                {"name": (Operators.LIKE, "%" + name_filter.get() + "%")}
            ),
        )

        # Academic qualifications
        academic_qualifications_filter = tk.StringVar()
        academic_qualifications_frame = tk.Frame(self)
        academic_qualifications_frame.pack(pady=10)
        self.create_filter(
            academic_qualifications_frame,
            "Search for academic qualifications like:",
            academic_qualifications_filter,
            lambda *args: self.filters["conditions"].update(
                {
                    "academic_qualifications": (
                        Operators.LIKE,
                        "%" + academic_qualifications_filter.get() + "%",
                    )
                }
            ),
        )

        # Department
        department_frame = tk.Frame(self)
        department_frame.pack(pady=10)
        self.create_dropdown(
            department_frame,
            self.departments,
            "Department",
            lambda department_id: self.filters["conditions"].update(
                {"department_id": (Operators.EQ, department_id)}
            ),
        )

        # Advisor of student
        advisor_of_frame = tk.Frame(self)
        advisor_of_frame.pack(pady=10)
        self.create_dropdown(
            advisor_of_frame,
            self.students,
            "Advisor of",
            lambda student_id: self.filters["conditions"].update(
                {"student_id": (Operators.EQ, student_id)}
            ),
        )

        # Program Filter
        program_frame = tk.Frame(self)
        program_frame.pack(pady=10)
        self.create_dropdown(
            program_frame,
            self.programs,
            "Program",
            lambda program_id: self.filters["conditions"].update(
                {"program_id": (Operators.EQ, program_id)}
            ),
        )

        # Expertise
        expertise_filter = tk.StringVar()
        expertise_frame = tk.Frame(self)
        expertise_frame.pack(pady=10)
        self.create_filter(
            expertise_frame,
            "Search for expertise like:",
            expertise_filter,
            lambda *args: self.filters["conditions"].update(
                {
                    "expertise": (
                        Operators.LIKE,
                        "%" + expertise_filter.get() + "%",
                    )
                }
            ),
        )

        # Expertise
        research_interests_filter = tk.StringVar()
        research_interests_frame = tk.Frame(self)
        research_interests_frame.pack(pady=10)
        self.create_filter(
            research_interests_frame,
            "Search for research interests like:",
            research_interests_filter,
            lambda *args: self.filters["conditions"].update(
                {
                    "research_interests": (
                        Operators.LIKE,
                        "%" + research_interests_filter.get() + "%",
                    )
                }
            ),
        )
