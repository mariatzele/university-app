from metadata import MetadataProvier

import tkinter as tk
from tkinter import ttk


class ListView:
    def __init__(self, primary, checked_boxes, record_data):
        self.primary = primary
        self.checked_boxes = checked_boxes

        # Create the Treeview
        self.treeview = self.create_listview()

        # Insert the initial data
        self.update_data(record_data)

    def create_listview(self):
        treeview = ttk.Treeview(self.primary, show="headings")
        # If metadata contains column info
        treeview = ttk.Treeview(
            self.primary, columns=self.checked_boxes, show="headings"
        )

        # Set up column headers and sorting
        for column in sorted(self.checked_boxes):
            if column not in self.checked_boxes:
                continue  # not showing this field
            treeview.heading(column, text=column)
            treeview.column(column, anchor="center", width=20)

        treeview.grid(row=2, column=1, padx=0, sticky="nsew")
        return treeview

    def update_data(self, data):
        """Clear and populate the Treeview with new data."""
        self.treeview.delete(*self.treeview.get_children())
        # Insert data into the Treeview
        # TESTING: test what happens if empty list.
        if data == None:
            return
        for item in data:
            column_values = [item[column] for column in self.treeview["columns"]]
            self.treeview.insert("", tk.END, values=column_values)

    def destroy(self):
        """Destroy the Treeview widget"""
        if self.treeview:
            self.treeview.destroy()
