import tkinter as tk
from gui.components import TreeView, ListView, FilterDialog
from data import (
    StudentRepository,
    CourseRepository,
    DepartmentRepository,
    LecturerRepository,
    StaffRepository,
    ProgramRepository,
    BaseRepository,
    Filter,
)
from metadata import MetadataProvider


class App:
    def __init__(
        self,
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
        # stores current table name and columns
        self.current_table = None
        self.active_table = "students"
        self.active_filter = Filter()
        self.metadata_provider = MetadataProvider(
            student_repo=student_repo,
            course_repo=course_repo,
            lecturer_repo=lecturer_repo,
            department_repo=department_repo,
            staff_repo=staff_repo,
        )

        self.reset_checkboxes()
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
            self.metadata_provider,
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
            self.metadata_provider,
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
        FilterDialog(
            self.app,
            self.active_table,
            self.handle_filter_apply,
            student_repo=self.student_repo,
            course_repo=self.course_repo,
            lecturer_repo=self.lecturer_repo,
            department_repo=self.department_repo,
            staff_repo=self.staff_repo,
            program_repo=self.program_repo,
        )

    def apply_search(self):
        query = self.search_var.get().lower()
        self.listview.filter_data(query)

    def get_data(self):
        repo = self.get_repo_for_active_table()
        if not repo:
            return []

        fields = [column for (column, _) in self.checked_boxes]
        return repo.search(self.active_filter, repo.map_fields(fields))

    def get_repo_for_active_table(self) -> BaseRepository:
        if self.active_table == "students":
            return self.student_repo
        elif self.active_table == "courses":
            return self.course_repo
        elif self.active_table == "departments":
            return self.department_repo
        elif self.active_table == "staff":
            return self.staff_repo
        elif self.active_table == "lecturers":
            return self.lecturer_repo
        else:
            return None

    def handle_filter_apply(self, filters):
        # map filters to table values
        filter = Filter()
        repo = self.get_repo_for_active_table()
        if not repo:
            return  # no matching repo found to query

        # map conditions
        mapped_filters_conditions = repo.map_filters(filters["conditions"])
        for column, (operator, value) in mapped_filters_conditions.items():
            if not value:
                continue
            if value == "NULL":  # handle NULL
                value = None
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
        if parent_name != self.active_table:
            self.set_active_table(parent_name)
            return
        for i in range(0, len(self.checked_boxes)):
            column, is_checked = self.checked_boxes[i]
            if column == checkbox_name:
                self.checked_boxes[i] = (column, not is_checked)
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
            self.reset_checkboxes()
            self.reload_table()

    def reset_checkboxes(self):
        columns = self.metadata_provider.get_table_metadata(self.active_table)[
            "column_names"
        ]
        self.checked_boxes = [(column, True) for column in columns]
