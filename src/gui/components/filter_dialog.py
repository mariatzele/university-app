import tkinter as tk
from data import Operators


class FilterDialog(tk.Toplevel):
    def __init__(self, parent, active_table, apply_filter_callback):
        self.active_table = active_table
        self.apply_filter_callback = apply_filter_callback
        self.filters = {"conditions": {}, "aggregates": {}}

        super().__init__(parent)  # Create a Toplevel window
        self.title("Filter Options")
        self.geometry("500x450")

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
        else:
            raise ValueError("invalid table name " + active_table)

        # Add Apply and Cancel buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        apply_button = tk.Button(button_frame, text="Apply", command=self.apply_filters)
        apply_button.pack(side="left", padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=self.destroy)
        cancel_button.pack(side="right", padx=5)

    def remove_filters(self):
        pass

    def apply_filters(self):
        self.apply_filter_callback(self.filters)
        self.destroy()

    def create_filter(
        self, frame, label_text, var, callback, widget_class=tk.Entry, **widget_options
    ):
        tk.Label(frame, text=label_text).pack(side="left", padx=5)
        widget = widget_class(frame, textvariable=var, **widget_options)
        widget.pack(side="left", padx=5)
        var.trace_add("write", callback)
        return widget

    def init_student_filters(self):
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

        # Advised by Lecturer ID Filter
        lecturer_filter = tk.StringVar()
        lecturer_frame = tk.Frame(self)
        lecturer_frame.pack(pady=10)
        self.create_filter(
            lecturer_frame,
            "Advised by Lecturer ID:",
            lecturer_filter,
            lambda *args: self.filters["conditions"].update(
                {"advised_by_lecturer_id": (Operators.EQ, int(lecturer_filter.get()))}
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

        # Program ID Filter
        program_filter = tk.StringVar()
        program_frame = tk.Frame(self)
        program_frame.pack(pady=10)
        self.create_filter(
            program_frame,
            "Program ID:",
            program_filter,
            lambda *args: self.filters["conditions"].update(
                {"program_id": (Operators.EQ, int(program_filter.get()))}
            ),
        )

        # Average grade filter
        program_filter = tk.StringVar()
        program_frame = tk.Frame(self)
        program_frame.pack(pady=10)
        self.create_filter(
            program_frame,
            "Average grade higher than:",
            program_filter,
            lambda *args: self.filters["aggregates"].update(
                {
                    "student_enrollments.grade": (  # can't use avg_grade here because it's in the SELECT
                        "AVG",
                        Operators.GT,
                        int(program_filter.get()),
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

        # Lecturer ID
        lecturer_filter = tk.StringVar()
        lecturer_frame = tk.Frame(self)
        lecturer_frame.pack(pady=10)
        self.create_filter(
            lecturer_frame,
            "Lecturer ID:",
            lecturer_filter,
            lambda *args: self.filters["conditions"].update(
                {"lecturer_id": (Operators.EQ, int(lecturer_filter.get()))}
            ),
        )

        # Department ID
        department_filter = tk.StringVar()
        department_frame = tk.Frame(self)
        department_frame.pack(pady=10)
        self.create_filter(
            department_frame,
            "Department ID:",
            department_filter,
            lambda *args: self.filters["conditions"].update(
                {"department_id": (Operators.EQ, int(department_filter.get()))}
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

        # Department ID
        department_filter = tk.StringVar()
        department_frame = tk.Frame(self)
        department_frame.pack(pady=10)
        self.create_filter(
            department_frame,
            "Department ID:",
            department_filter,
            lambda *args: self.filters["conditions"].update(
                {"department_id": (Operators.EQ, int(department_filter.get()))}
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
