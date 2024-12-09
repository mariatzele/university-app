import tkinter as tk
from metadata import MetadataProvier
from data import Filter, Operators


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
        if active_table == "courses":
            self.init_course_filters()
        else:
            print("TODO")

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
                {"name": (Operators.LIKE, name_filter.get() + "%")}
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
        # TODO
        return
