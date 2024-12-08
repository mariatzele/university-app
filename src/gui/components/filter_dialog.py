import tkinter as tk
from tkinter import ttk


class FilterDialog(tk.Toplevel):
    def __init__(self, parent, table_metadata, listview):
        super().__init__(parent)  # Create a Toplevel window
        self.title("Filter Options")
        self.geometry("300x200")

        # Store table metadata and reference to ListView
        self.table_metadata = table_metadata
        self.listview = listview  # Reference to the ListView to update

        # Add widgets to the dialog (example filters)
        ttk.Label(self, text="Select Filters:", font=("Arial", 12)).pack(pady=10)

        # Example filter checkboxes
        self.filter_1 = tk.BooleanVar()
        self.filter_2 = tk.BooleanVar()

        # PLACEHOLDER/TEST "Filter 1" will automatically filter for "marvin"
        ttk.Checkbutton(self, text="Search for 'marvin'",
                    variable=self.filter_1).pack(anchor="w", padx=20)
        ttk.Checkbutton(self, text="Filter 2",
        variable=self.filter_2).pack(
            anchor="w", padx=20)

        # Add Apply and Cancel buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        apply_button = ttk.Button(button_frame, text="Apply", command=self.apply_filters)
        apply_button.pack(side="left", padx=5)

        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.destroy)
        cancel_button.pack(side="right", padx=5)

    def remove_filters(self):
        pass

    def apply_filters(self):
        if self.filter_1.get():
            # Apply the "marvin" filter if Filter 1 is selected
            print("Filter 1 applied: Searching for 'marvin'")

            # Filter the data in ListView for "marvin" (case insensitive)
            filtered_data = [
                row for row in self.listview.filtered_data
                if
                any("marvin" in str(value).lower() for value in row.values())
            ]

            # Update the ListView with filtered data
            self.listview.update_data(filtered_data)

        if self.filter_2.get():
            print("Filter 2 is applied")

            # Close the dialog after applying filters
        self.destroy()


