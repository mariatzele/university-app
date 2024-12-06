import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
from tkinter import ttk
from PIL import Image, ImageTk



class TreeView:
    def __init__(self, primary, table_metadata):
        self.primary = primary

        # Path for images
        self.assets = os.path.join(os.path.dirname(__file__), '..',
                                   'assets')
        checked_image_path = os.path.join(self.assets, "checked_box.png")
        unchecked_image_path = os.path.join(self.assets, "unchecked_box.png")
        # Images
        self.checked_image = ImageTk.PhotoImage(
            Image.open(checked_image_path).resize((16, 16)))
        self.unchecked_image = ImageTk.PhotoImage(
            Image.open(unchecked_image_path).resize((16, 16)))

        # Create and configure a frame to hold the Treeview
        self.frame = ttk.Frame(self.primary)
        self.frame.grid(row=2, column=0, padx=20, pady=0, sticky="nsew")
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Create the Treeview widget with height parameter
        # Q: should this function be run under init?
        self.treeview = ttk.Treeview(self.frame, height=21)
        self.treeview.column("#0", width=100, anchor="w")

        # Place the Treeview using grid
        self.treeview.grid(row=2, column=0, sticky="nsew")
        # Set column headings
        self.treeview.heading("#0", text="Tables")

        # Insert parent and child nodes
        # Q: should this function be run under init?
        self.insert_nodes(table_metadata)

        # Bind the checkbox toggle function to mouse click
        self.treeview.bind("<Button-1>", self.toggle_checkbox)

    def insert_nodes(self, table_metadata):
        # Example function to insert nodes into the Treeview
        for table in table_metadata:
            self.treeview.insert("", "end", text=table)

    def select_table(self):
        """
        Returns a dictionary with keys "table_name" and "column_names".
        "column_names" is a list of columns selected in the treeview.
        Dictionary is passed to the listview.
        """

        # Need to add dialog pop-up

        # Find parent ID of selected item
        current_node = self.treeview.focus()
        if current_node == "":
            return
        parent_id = self.treeview.parent(current_node)
        if parent_id == "":
            parent_id = current_node

        # Get checked/selected child nodes from treeview
        child_ids = [item for item in self.treeview.get_children(parent_id) if
                     "checked" in self.treeview.item(item, "tags")]

        # Get table and column names
        child_names = [self.treeview.item(child_id, "text") for child_id in
                       child_ids]
        parent_name = self.treeview.item(parent_id, "text")

        # Create a dictionary of results to pass to the listview
        table_metadata = {"table_name": parent_name,
                               "column_names": child_names}
        return table_metadata


    def insert_nodes(self, table_metadata_list):
        """
        Insert nodes into the TreeView from table metadata.

        Args:
            table_metadata_list (list): A list of dictionaries where each dictionary
                                        has "table_name" as the parent and
                                        "column_names" as the children.
        """
        #********* NESTED FOR LOOP **********
        for metadata in table_metadata_list:
            # Extract the table name (parent) and column names (children)
            parent = metadata.get("table_name", "Unnamed Table")
            children = metadata.get("column_names", [])

            # Insert parent node
            parent_id = self.treeview.insert("", "end",
                                             text=parent)

            # Insert child nodes under the parent
            if isinstance(children, list):
                for child in children:
                    self.treeview.insert(parent_id, "end", text=child,
                                         tags = "checked",
                                         image=self.checked_image)

    def toggle_checkbox(self, event):

        # Identify the clicked row
        item = self.treeview.identify_row(event.y)
        # Exit if no valid row was clicked
        if not item:
            return

        # Retrieve current tags
        current_tags = self.treeview.item(item, "tags")
        # Toggle between 'checked' and 'unchecked'
        if  self.treeview.parent(item) == "":
            return
        elif "checked" in current_tags:
            self.treeview.item(item, image = self.unchecked_image,
                               tags=('unchecked',))
            print(f"Unchecked: {self.treeview.item(item, 'text')}")
        else:
            self.treeview.item(item, image = self.checked_image,
                               tags=('checked',))
            # self.treeview.item(self.treeview.parent(item), image = self.checked_image,
            #                    tags=('checked',))
            print(f"Checked: {self.treeview.item(item, 'text')}")


