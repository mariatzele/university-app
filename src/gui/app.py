import tkinter as tk
from gui.components import TreeView, ListView, FilterDialog
from data import (
    StudentRepository,
    CourseRepository,
    DepartmentRepository,
    LecturerRepository,
    Filter,
)
from metadata import MetadataProvier


class App:
    def __init__(
        self,
        student_repo: StudentRepository,
        course_repo: CourseRepository,
        lecturer_repo: LecturerRepository,
        department_repo: DepartmentRepository,
    ):
        self.student_repo = student_repo
        self.course_repo = course_repo
        self.lecturer_repo = lecturer_repo
        self.department_repo = department_repo
        # stores current table name and columns
        self.current_table = None
        self.active_table = "students"
        self.active_filter = Filter()
        self.checked_boxes = MetadataProvier().get_table_metadata(self.active_table)[
            "column_names"
        ]

        self.build_app()  # Initialize the app window (self.app)

    def start(self):
        self.app.mainloop()

    def build_app(self):
        # Create the main Tkinter window
        self.app = tk.Tk()
        self.app.geometry("1200x600")
        self.app.title("Dashboard")

        # Configure grid layout
        self.app.grid_rowconfigure(0, weight=0)  # Dashboard header
        self.app.grid_rowconfigure(1, weight=0)  # Top bar
        self.app.grid_rowconfigure(2, weight=1)  # Main content row
        self.app.grid_columnconfigure(1, weight=4)  # Main content column
        self.app.grid_columnconfigure(0, weight=1)  # Sidebar column
        self.app.grid_rowconfigure(0, weight=1)  # Sidebar row
        self.app.grid_rowconfigure(3, weight=0)  # Footer bar row

        # Dashboard header
        # Create a frame for the header (row 0)
        self.top_bar = tk.Frame(self.app, bg="gray", height=40)
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        # Add content to the top bar
        top_bar_label = tk.Label(
            self.top_bar, text="Dashboard", fg="white", bg="gray", font=("Arial", 16)
        )
        top_bar_label.pack(padx=10, pady=5, side="left")

        # Top bar
        # Create a frame for the search bar and filter button (row 1 column 1)
        self.top_bar_frame = tk.Frame(self.app)
        self.top_bar_frame.grid(
            row=1, column=1, columnspan=1, padx=20, pady=10, sticky="ew"
        )

        # Main frame
        # Create a main frame (row 2)
        self.main_frame = tk.Frame(self.app, borderwidth=2, height=100)
        self.main_frame.grid(
            row=2, column=0, columnspan=2, padx=20, pady=20, sticky="nsew"
        )
        # Create the Treeview widget and add it to the main frame
        self.treeview = TreeView(
            self.app,
            self.active_table,
            self.set_active_table,
            self.handle_checkbox,
            self.checked_boxes,
        )
        # Create the ListView widget and add it to the main frame
        self.listview = ListView(self.app, self.checked_boxes, self.get_data())

        # Footer
        # Create a frame for the footer bar (row 3)
        self.footer_bar = tk.Frame(self.app, height=30)
        self.footer_bar.grid(row=3, column=1, columnspan=2, sticky="ew")
        # Create a frame for the apply button (row 3 column 0)
        self.footer_bar = tk.Frame(self.app)
        self.footer_bar.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        # Add the filter button
        self.filter_button = tk.Button(
            self.top_bar_frame, text="Filter", command=self.apply_filter
        )
        self.filter_button.pack(padx=10, pady=5, side="right")
        # Add the Apply button to the footer bar
        self.button = tk.Button(
            self.footer_bar, text="Apply", command=self.reload_table
        )
        self.button.pack(padx=10, pady=10, side="right")

    def reload_table(self):
        """
        This method reloads the data for the table
        """
        # Destroy the existing ListView before creating a new one
        if self.listview:
            self.listview.destroy()

        if self.treeview:
            self.treeview.destroy()

        # Create and display the ListView with the table metadata
        self.listview = ListView(self.app, self.checked_boxes, self.get_data())
        self.treeview = TreeView(
            self.app,
            self.active_table,
            self.set_active_table,
            self.handle_checkbox,
            self.checked_boxes,
        )

    def apply_filter(self):
        """
        This method is triggered when the filter button is clicked.
        It calls the table_selection method from TreeView, which gets the
        selected table metadata.
        Then it opens the FilterDialog with the retrieved metadata.
        """
        FilterDialog(self.app, self.active_table, self.handle_filter_apply)

    def apply_search(self):
        query = self.search_var.get().lower()
        self.listview.filter_data(query)

    def get_data(self):
        if self.active_table == "students":
            return self.student_repo.search(
                self.active_filter, self.student_repo.map_fields(self.checked_boxes)
            )
        if self.active_table == "courses":
            return self.course_repo.search(
                self.active_filter, self.course_repo.map_fields(self.checked_boxes)
            )
        if self.active_table == "departments":
            return self.department_repo.search(
                self.active_filter, self.department_repo.map_fields(self.checked_boxes)
            )
        return []

    def handle_filter_apply(self, filters):
        # map filters to table values
        filter = Filter()
        repo = None
        if self.active_table == "students":
            repo = self.student_repo
        if self.active_table == "courses":
            repo = self.course_repo
        if self.active_table == "departments":
            repo = self.department_repo
        if not repo:
            return  # no matching repo found to query

        # map conditions
        mapped_filters_conditions = repo.map_filters(filters["conditions"])
        for column, (operator, value) in mapped_filters_conditions.items():
            if not value:
                continue
            filter.add_condition(column, operator, value)

        for column, (
            aggregate_op,
            condition_op,
            value,
        ) in filters["aggregates"].items():
            if not value:
                continue
            filter.add_aggregate_condition(column, aggregate_op, condition_op, value)

        self.active_filter = filter
        self.reload_table()

    def handle_checkbox(self, checkbox_name, parent_name):
        # this checkbox belongs to different table - update the list first
        print(checkbox_name, parent_name)
        if parent_name != self.active_table:
            self.set_active_table(parent_name)
            return
        if checkbox_name in self.checked_boxes:
            self.checked_boxes.remove(checkbox_name)
        else:
            self.checked_boxes.append(checkbox_name)
        self.reload_table()  # updated fields need to reload data

    def set_active_table(self, table):
        prev = self.active_table
        if table == "students":
            self.active_table = "students"
        if table == "courses":
            self.active_table = "courses"
        if table == "departments":
            self.active_table = "departments"
        if table == "staff":
            self.active_table = "staff"
        if table == "lecturers":
            self.active_table = "lecturers"

        if prev != self.active_table:
            self.active_filter = Filter()  # clear filter
            # set all checkboxes to true
            self.checked_boxes = MetadataProvier().get_table_metadata(
                self.active_table
            )["column_names"]
            self.reload_table()
