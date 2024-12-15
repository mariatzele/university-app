"""listview.py"""
import tkinter as tk
from tkinter import ttk


class ListView:
    """
    A class representing a Treeview-based list view widget.
    """
    def __init__(self, primary, checked_boxes, record_data):
        self.primary = primary
        self.checked_boxes = checked_boxes
        self.record_data = record_data

        # Create the Treeview
        self.treeview = self.create_listview()

        # Insert  data
        self.update_data()

    def create_listview(self):
        """
        Create and configure the list view widget based on checked columns.
        """
        columns = [column for column, is_checked in self.checked_boxes if is_checked]
        # treeview = ttk.Treeview(self.primary, show="headings")
        # If metadata contains column info
        treeview = ttk.Treeview(self.primary, columns=columns, show="headings")

        # Set up column headers
        for column in columns:
            treeview.heading(column, text=column)
            treeview.column(column, anchor="center", width=20)

        if len(self.record_data) > 0:
            for column in columns:
                max_length = max(len(str(item[column])) for item in self.record_data)
                treeview.column(
                    column, width=min(max(10, max_length * 10), 50)
                )  # Adjust width

        treeview.grid(row=2, column=1, padx=20, sticky="nsew")
        return treeview

    def update_data(self):
        """Clear and populate the Treeview with new data."""
        self.treeview.delete(*self.treeview.get_children())
        # Insert data into the Treeview
        if self.record_data is None:
            return
        for item in self.record_data:
            column_values = [item[column] for column in self.treeview["columns"]]
            self.treeview.insert("", tk.END, values=column_values)

    def destroy(self):
        """Destroy the Treeview widget"""
        if self.treeview:
            self.treeview.destroy()
