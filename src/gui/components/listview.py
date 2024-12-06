from dummy_data import student_records
from dummy_data import course_records


import tkinter as tk
from tkinter import ttk

class ListView:
    def __init__(self, primary, table_metadata={}, record_data=[]):

        # Record_data not used for intial data input. Would it be better to
        # pass the argument in one of the methods? Or should this class be
        # redesigned entirely?
        self.primary = primary
        self.metadata = table_metadata

        # Initialize data storage
        self.initial_data = self.initial_data()  # Full dataset
        self.filtered_data = self.initial_data

        print(self.initial_data)
        # self.filtered_data = record_data  # Initially, filtered data is the same as the original

        # Column sorting
        self.sort_column = None  # Last sorted column
        self.sort_order = False  # False = ascending, True = descending

        # Create the Treeview
        self.treeview = self.create_listview()

        # Insert the initial data
        self.update_data(self.initial_data)

    def create_listview(self):
        treeview = ttk.Treeview(self.primary, show='headings')

        if self.metadata:  # If metadata contains column info
            columns = self.metadata.get("column_names", [])
            treeview = ttk.Treeview(self.primary, columns=columns, show='headings')

            # Set up column headers and sorting
            for column in columns:
                treeview.heading(column, text=column, command=lambda c=column: self.sort_data(c))
                treeview.column(column, anchor="center")

        treeview.grid(row=2, column=1, sticky="nsew")
        return treeview

    def initial_data(self):
        #*******Placeholder code*******
        """checks the table name and columns returned by the treeview and
        returns the corresponding data."""
        # pulls directly from the class parameters
        # ****** NESTED IFS *******
        # if not record_data or record_data == []:
        table = self.metadata.get("table_name")  # Now it should correctly reference the instance attribute
        if table == "Students":
            print(student_records)  # Ensure you have student_records defined somewhere in your code
            return student_records
        if table == "Courses":
            print(course_records)  # Ensure you have course_records defined somewhere in your code
            return course_records
        return []

    def update_data(self, data):
        """Clear and populate the Treeview with new data."""
        self.treeview.delete(*self.treeview.get_children())  # Clear existing rows
        # Insert data into the Treeview
        # TESTING: test what happens if empty list.
        if data == None:
            return
        for item in data:
            column_values = [item[column] for column in self.treeview["columns"]]
            self.treeview.insert("", tk.END, values=column_values)  # Insert row into Treeview

    def filter_data(self, query):
        """Filter data based on a query string and update the Treeview."""
        # I suspect this may need redoing or a new one based on the filter
        # system
        query = query.lower()
        self.filtered_data = [
            row for row in self.initial_data
            if any(query in str(value).lower() for value in row.values())
        ]
        self.update_data(self.filtered_data)

    def sort_data(self, column):
        """Sort the data based on the clicked column."""
        if column == self.sort_column:
            self.sort_order = not self.sort_order  # Toggle order
        else:
            self.sort_column = column
            self.sort_order = False  # Default to ascending

        self.filtered_data.sort(
            key=lambda x: str(x[column]).lower(), reverse=self.sort_order
        )
        self.update_data(self.filtered_data)

    def destroy(self):
        """ Destroy the Treeview widget"""
        if self.treeview:
            self.treeview.destroy()
            print("Listview destroyed.")