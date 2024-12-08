import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
)
from tkinter import ttk
from PIL import Image, ImageTk
from metadata import MetadataProvier


class TreeView:
    def __init__(
        self,
        primary,
        active_table,
        table_change_callback,
        checkbox_change_callback,
        checked_boxes,
    ):
        self.primary = primary
        self.active_table = active_table
        self.table_change_callback = table_change_callback
        self.checkbox_change_callback = checkbox_change_callback
        self.table_metadata = MetadataProvier().get_all_table_metadata()
        self.checked_boxes = checked_boxes

        # Path for images
        self.assets = os.path.join(os.path.dirname(__file__), "..", "assets")
        checked_image_path = os.path.join(self.assets, "checked_box.png")
        unchecked_image_path = os.path.join(self.assets, "unchecked_box.png")
        # Images
        self.checked_image = ImageTk.PhotoImage(
            Image.open(checked_image_path).resize((16, 16))
        )
        self.unchecked_image = ImageTk.PhotoImage(
            Image.open(unchecked_image_path).resize((16, 16))
        )

        # Create and configure a frame to hold the Treeview
        self.frame = ttk.Frame(self.primary)
        self.frame.grid(row=2, column=0, padx=20, pady=0, sticky="nsew")
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Create the Treeview widget with height parameter
        # Q: should this function be run under init?
        self.treeview = ttk.Treeview(self.frame, height=21)
        self.treeview.column("#0", width=100, anchor="w")
        self.treeview.bind("<ButtonRelease-1>", self.handle_node_click)

        # Place the Treeview using grid
        self.treeview.grid(row=2, column=0, sticky="nsew")
        # Set column headings
        self.treeview.heading("#0", text="Tables")

        self.insert_nodes()

        # Bind the checkbox toggle function to mouse click
        self.treeview.bind("<Button-1>", self.toggle_checkbox)

    def handle_node_click(self, event):
        item = self.treeview.selection()
        if item:
            self.table_change_callback(self.treeview.item(item[0], "text"))

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
        child_ids = [
            item
            for item in self.treeview.get_children(parent_id)
            if "checked" in self.treeview.item(item, "tags")
        ]

        # Get table and column names
        child_names = [self.treeview.item(child_id, "text") for child_id in child_ids]
        parent_name = self.treeview.item(parent_id, "text")

        # Create a dictionary of results to pass to the listview
        table_metadata = {"table_name": parent_name, "column_names": child_names}
        return table_metadata

    def insert_nodes(self):
        """
        Insert nodes into the TreeView from table metadata.
        A list of dictionaries where each dictionary has "table_name" as the
        parent and "column_names" as the children.
        """
        for metadata in self.table_metadata:
            # Extract the table name (parent) and column names (children)
            parent = metadata.get("table_name")
            children = metadata.get("column_names")

            # Insert parent node
            parent_id = self.treeview.insert(
                "", "end", text=parent, open=parent == self.active_table
            )

            # Insert child nodes under the parent
            for child in children:
                is_checked = True if child in self.checked_boxes else False
                self.treeview.insert(
                    parent_id,
                    "end",
                    text=child,
                    tags="checked" if is_checked else "unchecked",
                    image=self.checked_image if is_checked else self.unchecked_image,
                )

    def toggle_checkbox(self, event):
        # Identify the clicked row
        item = self.treeview.identify_row(event.y)
        # Exit if no valid row was clicked
        if not item:
            return
        parent = self.treeview.parent(item)
        if not parent:
            return
        else:
            self.checkbox_change_callback(
                self.treeview.item(item, "text"), self.treeview.item(parent, "text")
            )

    def destroy(self):
        """Destroy the Treeview widget"""
        if self.treeview:
            self.treeview.destroy()
