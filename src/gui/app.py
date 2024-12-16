"""
app.py
A module that contains the main application class for managing the
University Records Database.
"""
import tkinter as tk
from tkinter import ttk
from tktooltip import ToolTip

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
    """
    The main application class for managing the University Records Database.
    It initializes the GUI components and manages the interactions between
    the repositories and the interface.
    """
    def __init__(
        self,
        student_repo: StudentRepository,
        course_repo: CourseRepository,
        lecturer_repo: LecturerRepository,
        department_repo: DepartmentRepository,
        staff_repo: StaffRepository,
        program_repo: ProgramRepository,
    ):
        """
       Initializes the App with the required repositories.

       Parameters:
           student_repo (StudentRepository): Repository for student data.
           course_repo (CourseRepository): Repository for course data.
           lecturer_repo (LecturerRepository): Repository for lecturer data.
           department_repo (DepartmentRepository): Repository for department data.
           staff_repo (StaffRepository): Repository for staff data.
           program_repo (ProgramRepository): Repository for program data.
       """

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
        """Starts the application"""
        self.app.mainloop()

    def build_app(self):
        """
        Builds the GUI components for the application, including the main window,
        header, top bar, main frame, and footer.
        """
        bg_colour = "#c8b9c3" # background colour

        # Create the main Tkinter window
        self.app = tk.Tk()
        self.app.geometry("1200x600")
        self.app.title("University Records Database Application")
        self.app.configure(bg=bg_colour)

        # Configure grid layout
        self.app.grid_rowconfigure(0, weight=1, minsize=50)  # header
        self.app.grid_rowconfigure(1, weight=0)  # Top bar
        self.app.grid_rowconfigure(2, weight=1)  # Main content row
        self.app.grid_columnconfigure(1, weight=4)  # Main content column
        self.app.grid_columnconfigure(0, weight=1)  # Sidebar column
        self.app.grid_rowconfigure(0, weight=1)  # Sidebar row
        self.app.grid_rowconfigure(3, weight=0)  # Footer bar row

        # Dashboard header
        db_colour = "#4f064a"
        # Create a frame for the header (row 0)
        self.header = tk.Frame(self.app, bg=db_colour)
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew")

        # self.header.grid_propagate(False)
        # Add content to the dashboard ***************
        header_logo = tk.Label(self.header, text="ABC UNIVERSITY", fg="white",
                               bg=db_colour, font=("Arial", 16))
        header_logo.pack(padx=10, pady=10, side="left")


        # Top bar
        # Create a frame for the search bar and filter button (row 1 column 1)
        self.top_bar_frame = tk.Frame(self.app, bg=bg_colour)
        self.top_bar_frame.grid(row=1, column=1, columnspan=1, padx=20,
                                pady=10, sticky="ew")

        # Main frame
        # Create a main frame (row 2)
        self.main_frame = tk.Frame(self.app, borderwidth=2, height=100,
                                   bg=bg_colour)
        self.main_frame.grid(row=2, column=0, columnspan=2, padx=20,
                             pady=20, sticky="nsew")

        # Configure ttk style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Treeview.Frame', background=bg_colour)
        self.style.configure('TFrame', background=bg_colour)

        # Create and configure a frame to hold the Treeview
        self.frame = ttk.Frame(self.app)
        self.frame.grid(row=2, column=0, padx=20, pady=0, sticky="nsew")
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        # Footer
        # Create a frame for the footer bar (row 3)
        self.footer_bar = tk.Frame(self.app, height=40, bg=bg_colour)
        self.footer_bar.grid(row=3, column=0, columnspan=2, sticky="ew")

        # Add the filter button
        self.filter_button = ttk.Button(self.top_bar_frame,
                                        text="Filter",
                                        command=self.apply_filter)
        self.filter_button.pack(padx=10, pady=5, side="right")

        # Key bindings
        self.filter_button.bind("<Return>",
                                lambda event: self.apply_filter())

        # ToolTips
        ToolTip(widget=self.filter_button, msg="Filter table", delay=1.0)

        # Create the Treeview widget and add it to the main frame
        self.treeview = TreeView(
            self.metadata_provider,
            self.frame,
            self.active_table,
            self.set_active_table,
            self.handle_checkbox,
            self.checked_boxes,
        )
        # Create the ListView widget and add it to the main frame
        self.listview = ListView(self.app, self.checked_boxes, self.get_data())


    def reload_table(self):
        """
        Reloads the data for the table by destroying and recreating the
        ListView and TreeView widgets.
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
            self.frame,
            self.active_table,
            self.set_active_table,
            self.handle_checkbox,
            self.checked_boxes,
        )

    def apply_filter(self):
        """ Opens the FilterDialog with table, filter and repo data """
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

    def get_data(self):
        """
        Retrieves data from the active repository.
        Returns repo data with filtered columns
        """
        repo = self.get_repo_for_active_table()
        if not repo:
            return []

        fields = [column for (column, _) in self.checked_boxes]
        return repo.search(self.active_filter, repo.map_fields(fields))

    def get_repo_for_active_table(self) -> BaseRepository:
        """
        Returns the repository corresponding to the currently active table.
        """
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
        """Applies filters and reloads the table with filtered data."""
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
        """ Resets checkboxes and active table """
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
        """
        Sets the active table for operations. If the new active table is
        different from the current one, it resets the active filter, resets
        checkboxes, and reloads the table.
        """
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
        """resets checkboxes for active table"""
        columns = self.metadata_provider.get_table_metadata(self.active_table)[
            "column_names"
        ]
        self.checked_boxes = [(column, True) for column in columns]
