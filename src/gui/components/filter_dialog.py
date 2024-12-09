import tkinter as tk
from metadata import MetadataProvier
from data import Filter, Operators


class FilterDialog(tk.Toplevel):
    def __init__(self, parent, active_table, apply_filter_callback):
        self.active_table = active_table
        self.apply_filter_callback = apply_filter_callback
        self.filters = {}

        super().__init__(parent)  # Create a Toplevel window
        self.title("Filter Options")
        self.geometry("300x200")

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

    def init_student_filters(self):
        # name
        name_filter = tk.StringVar()
        name_filter.trace_add(
            "write",
            lambda *args: self.filters.update(
                {
                    "name": (Operators.LIKE, name_filter.get() + "%")
                }  # Need % to do fuzzy matching
            ),
        )
        name_frame = tk.Frame(self)
        name_frame.pack(pady=10)

        name_label = tk.Label(name_frame, text="Search for name like:")
        name_label.pack(side="left", padx=5)  # Add some padding

        name_entry = tk.Entry(name_frame, textvariable=name_filter, width=10)
        name_entry.pack(side="left", padx=5)

        year_filter = tk.StringVar()
        year_filter.trace_add(
            "write",
            lambda *args: self.filters.update(
                {"year_of_study": (Operators.EQ, year_filter.get())}
            ),
        )
        year_frame = tk.Frame(self)
        year_frame.pack(pady=10)

        year_label = tk.Label(year_frame, text="Year of Study:")
        year_label.pack(side="left", padx=5)  # Add some padding

        year_entry = tk.Entry(year_frame, textvariable=year_filter, width=10)
        year_entry.pack(side="left", padx=5)

    def init_course_filters(self):
        # TODO
        return
