import tkinter as tk
from gui.components.treeview import TreeView
from gui.components.listview import ListView
from gui.components.filter_dialog import FilterDialog
from tkinter import ttk

from dummy_data import table_metadata_dict_list

class MainWindow:
    def __init__(self):

        # stores current table name and columns
        self.current_table = None

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
        self.app.grid_rowconfigure(0, weight=1) # Sidebar row
        self.app.grid_rowconfigure(3, weight=0)  # Footer bar row

        # Dashboard header
        # Create a frame for the header (row 0)
        self.top_bar = tk.Frame(self.app, bg="gray", height=40)
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        # Add content to the top bar
        top_bar_label = tk.Label(self.top_bar, text="Dashboard", fg="white",
                                 bg="gray", font=("Arial", 16))
        top_bar_label.pack(padx=10, pady=5, side="left")

        # Top bar
        # Create a frame for the search bar and filter button (row 1 column 1)
        self.search_bar_frame = tk.Frame(self.app)
        self.search_bar_frame.grid(row=1, column=1, columnspan=1, padx=20,
                                   pady=10, sticky="ew")

        # Main frame
        # Create a main frame (row 2)
        self.main_frame = tk.Frame(self.app, borderwidth=2, height=100)
        self.main_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
        # Create the Treeview widget and add it to the main frame
        self.treeview = TreeView(self.app, table_metadata_dict_list)
        # Create the ListView widget and add it to the main frame
        self.listview = ListView(self.app)


        #Footer
        # Create a frame for the footer bar (row 3)
        self.footer_bar = tk.Frame(self.app, height=30)
        self.footer_bar.grid(row=3, column=1, columnspan=2, sticky="ew")
        # Create a frame for the apply button (row 3 column 0)
        self.footer_bar = ttk.Frame(self.app)
        self.footer_bar.grid(row=3, column=0, padx=20, pady=5, sticky="ew")


        # Buttons, search bar and key bindings
        # Add the search bar
        self.search_var = tk.StringVar()
        search_bar = ttk.Entry(self.search_bar_frame,
                               textvariable=self.search_var, font=("Arial", 12))
        search_bar.pack(padx=1, pady=5, side="left")
        # Bind the 'Enter' key to the search bar
        search_bar.bind("<Return>", lambda event: self.apply_search())
        # Add the Search button to the
        self.filter_button = ttk.Button(self.search_bar_frame, text="Search",
                                        command=self.apply_search)
        self.filter_button.pack(padx=10, pady=5, side="left")
        # Add the filter button
        self.filter_button = ttk.Button(self.search_bar_frame,
                                        text="Filter", command=self.apply_filter)
        self.filter_button.pack(padx=10, pady=5, side="right")
        # Add the Apply button to the footer bar
        self.button = ttk.Button(self.footer_bar, text="Apply",
                                 command=self.apply_table)
        self.button.pack(padx= 10, pady=10, side="right")


    def apply_table(self):
        """
        This method is triggered when the Apply button is clicked.
        It calls the table_selection method from TreeView, which returns the
        selected table metadata (table name and columns).
        Then it opens the ListView with the retrieved metadata.
        """
        # Add error control

        # Call table_selection to get the table name and columns
        table_metadata = self.treeview.select_table()
        if not table_metadata or table_metadata == {}:
            print("No table selected")
            return

        # Destroy the existing ListView before creating a new one
        # Q: Should this be in the listview module?
        if self.listview:
            self.listview.destroy()

        # Create and display the ListView with the table metadata
        self.listview = ListView(self.app, table_metadata)

        # persistent storage of table name and columns
        self.current_table = table_metadata


    def apply_filter(self):
        """
        This method is triggered when the filter button is clicked.
        It calls the table_selection method from TreeView, which gets the
        selected table metadata.
        Then it opens the FilterDialog with the retrieved metadata.
        """
        print("apply filter")
        print(self.current_table)
        FilterDialog(self.app, self.current_table, self.listview)

    def apply_search(self):
        query = self.search_var.get().lower()
        self.listview.filter_data(query)





# Create an instance of the main window and start the app
app = MainWindow()
app.start()












