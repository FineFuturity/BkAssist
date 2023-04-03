import os
import re
import openpyxl
import tkinter as tk
import pandas as pd
from tkinter import ttk
from tkinter import filedialog
from operator import itemgetter

filetypes = [
               ("Excel Workbook and .CSV files", "*.csv;*.xlsx;*.xls"),
               ("Comma-separated Values file", "*.csv"),
               ("Excel Workbook file", "*.xlsx;*.xls")
            ]

class FilterableTreeviewApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Auditing Utility")
        self.geometry("1024x768")
        self.load_menubar()

        self.curr_file = None
        self.df = None
        self.all_items = None
        self.sort_direction = None

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_treeview)

        self.sidebar = tk.Frame(self, width=275, borderwidth=1, relief="sunken")
        self.sidebar.pack(side="right", fill="y")

        self.top_frame = tk.Frame(self.sidebar, width=275, borderwidth=1, relief="solid")
        self.top_frame.pack(side="top", fill="x", padx=10, pady=10)

        self.main_content = tk.Frame(self)
        self.main_content.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        # self.vscrframe = tk.Frame(self.main_content, width=3, borderwidth=1, relief="solid")

        self.search_entry = tk.Entry(self.main_content, textvariable=self.search_var)

        self.treeview = ttk.Treeview(self.main_content, columns=("col1", "col2"), show="headings")
        self.treeview.heading("col1", text="Column 1")
        self.treeview.heading("col2", text="Column 2")

         # Create a horizontal scrollbar
        self.h_scrollbar = ttk.Scrollbar(self.main_content, orient="horizontal", command=self.treeview.xview)

        # Create a vertical scrollbar
        self.v_scrollbar = ttk.Scrollbar(self.main_content, orient="vertical", command=self.treeview.yview)
        

        # Bind the Treeview widget to the double-click event handler
        self.treeview.bind("<Double-1>", lambda event: self.on_double_click(event))

    def on_double_click(self, event):
        # destroy any widget in the top_frame if one is there
        for widget in self.top_frame.winfo_children():
            widget.destroy()

        # Get the item that was clicked
        item = self.treeview.selection()[0]
        # print("iid should be: ", item[0])

        # Get the values of the selected row
        values = self.treeview.item(item)['values']

        # Create a Treeview widget in the Toplevel window
         # Create a horizontal scrollbar
        top_tree = ttk.Treeview(self.top_frame, columns=("Attributes", "Data"), show="headings")
        topv_scrollbar = ttk.Scrollbar(self.top_frame, orient="vertical", command=self.treeview.yview)
        #Configure the Treeview to use the scrollbars
        top_tree.configure(yscrollcommand=topv_scrollbar.set)

        topv_scrollbar.pack(side="right", fill="y", expand=True, padx=2)

        # Pack the Treeview widget
        top_tree.pack(fill='x', expand=True, padx=5, pady=5)

        attrhdr = 'Attributes'
        # create and format the two columns for population of the selected row data
        top_tree.heading(attrhdr, text='Attributes', anchor="e")
        top_tree.heading('Data', text='Data', anchor="w")
        top_tree.column('Attributes', anchor="e", width=100)
        top_tree.column('Data', anchor="w", width=140)

        for idx, val in enumerate(values):
            col_name = self.treeview.heading(idx)['text']
            top_tree.insert('', 'end', text='', values=(col_name, val))


    def load_menubar(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=lambda: self.file_from_usr())
    
    def det_csv_enc(self, file_path):
        # Open the file in binary mode and read a small amount of the contents
        with open(file_path, "rb") as f:
            contents = f.read(1000)

        # Detect the encoding of the contents using chardet
        result = cd.detect(contents)
        encoding = result["encoding"]

        return encoding

    def file_from_usr(self):
        # Prompt the user to select a file
        file_path = tk.filedialog.askopenfilename(parent=self,
            title="Select a file",
            filetypes=filetypes
        )
    
        self.curr_file, file_extension = os.path.splitext(file_path)
        file_name = file_path.split("/")[-1]

        if file_extension == ".csv":
            # Read data from CSV file into a pandas DataFrame
            encoding = self.det_csv_enc(file_path)
            try:
                self.df = pd.read_csv(file_path, encoding=encoding, dtype=str)
                self.df['row_id'] = self.df.index
            except:
                self.cur_file = None
                tk.messagebox.showerror(f"Error Loading file: {file_name}{file_extension}", f"Unable to read file with {encoding} encoding. Please ")
        elif file_extension in (".xlsx", ".xls"):
            # Read data from Excel file into a pandas DataFrame
            self.df = pd.read_excel(file_path, dtype=str)
        else:
            # Show an error message if the file type is not supported
            tk.messagebox.showerror("Error", "Unsupported file type")
            exit()
        
        # Replace NaN values with an empty string
        self.df.fillna(' ', inplace=True)
        # print(self.df)

        # clear top frame in case one was loaded from previous session
        for widget in self.top_frame.winfo_children():
            widget.destroy()

        #clear the treeview to start a new session
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        self.treeview["columns"] = tuple(self.df.columns)

        self.populate_treeview()

    def sort_column(self, col):
        # Get the current items in the treeview
        items = self.treeview.get_children()

        # Extract the values for the specified column
        column_values = [(self.treeview.set(item, col), item) for item in items]

        # Sort the items based on the column values
        sort_key = itemgetter(0)

        # print("dir is: " + self.sort_direction[col])
        if self.sort_direction[col] == "ascending":
            sorted_items = sorted(column_values, key=sort_key)
            self.sort_direction[col] = "descending"
        elif self.sort_direction[col] == "descending":
            sorted_items = sorted(column_values, key=sort_key, reverse=True)
            self.sort_direction[col] = "original"
        else:  # "original"
            # Clear the treeview
            for item in items:
                self.treeview.delete(item)
                
            # if search box is empty, rebuild the treeview with the original data
            # Add data to the Treeview
            for idx, row in self.df.iterrows():
                iid = str(idx)
                self.treeview.insert("", "end", iid=iid, values=tuple(row))

            # Reset the sort direction for the column
            self.sort_direction[col] = "ascending"
            return

            # Rearrange the items in the treeview
        for index, (_, item) in enumerate(sorted_items):
            self.treeview.move(item, "", index)

    def populate_treeview(self):
         # Set the column headings
        for col in self.df.columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, anchor="center")

        # Add data to the Treeview
        for idx, row in self.df.iterrows():
            iid = str(idx)
            self.treeview.insert("", "end", iid=iid, values=tuple(row))

        #prevent the empty iid column from appearing
        # if not dev:
        #self.treeview["show"] = "headings"
        self.treeview.heading('#1', anchor="e")
        self.treeview.column('#1', anchor="e", width=100)

        for col in self.treeview["columns"]:
            self.treeview.heading(col, text=col, command=lambda col=col: self.sort_column(col))
        
        # Configure the Treeview to use the scrollbars
        self.treeview.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)

        # Pack the Treeview widget
        self.search_entry.pack(fill="x", padx=5, pady=5)
        self.h_scrollbar.pack(side="bottom", fill="x")
        self.v_scrollbar.pack(side="right", fill="y")
        self.treeview.pack(expand=True, fill=tk.BOTH)

        self.sort_direction = {col: "ascending" for col in self.treeview["columns"]}

    # def filter_treeview(self, *args):
    #     search_term = self.search_var.get().lower()
    #     # regexpr = r'\b\w+\b|\d{4}-\d{2}-\d{2}|\s\d{2}:\d{2}:\d{2}\.\d{6}'
    #     # regexpr = r'\b\w+\b|\d{4}-\d{2}-\d{2}'
    #     # regexpr = r'\b\w+\b|\d{4}-\d{2}-\d{2}|\d{2}:\d{2}:\d{2}\.\d{6}'
    #     regexpr = r'\b\w+\b'

    #     # Split the search term into words
    #     search_words = re.findall(regexpr, search_term)

    #     # Clear the treeview
    #     for item in self.treeview.get_children():
    #         self.treeview.delete(item)

    #     self.treeview["show"] = "headings"

    #     # Re-insert items that match the search term
    #     for item in self.df.itertuples():
    #         item_values = [str(value).lower() for value in item]

    #         # Split the item values into words
    #         item_words = [re.findall(regexpr, value) for value in item_values]

    #         # Flatten the list of item words
    #         item_words = [word for words in item_words for word in words]

    #         # Check if all search words are present in the item_words
    #         #if all(word in item_words for word in search_words):
    #         # if all(any(word.startswith(search_word) for word in item_words) for search_word in search_words):
    #         if all(any(word == search_word for word in item_words) for search_word in search_words):
    #             self.treeview.insert("", "end",  iid=item[0], values=item[1:])

    def filter_treeview(self, *args):
        search_term = self.search_var.get().lower()
        search_tokens = search_term.split()

        # Clear the treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        # self.treeview["show"] = "headings"

        # Set the column headings
        for col in self.df.columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, anchor="center")

        self.treeview.heading('#1', anchor="e")

        # Re-insert items that match the search term
        for item in self.df.itertuples():
            item_values = [str(value).lower() for value in item][1:]
            # print(item_values)
            # print("result:", item_values)

            # Tokenize the values by splitting on commas and spaces
            item_tokens = []
            for value in item_values:
                tokens = value.replace(',', '').split()
                item_tokens.extend(tokens)

            # If all search_tokens are in item_tokens, insert the item
            # if all(search_token in item_tokens for search_token in search_tokens):
            if all(search_token in item_tokens for search_token in search_tokens):
            # if all(any(search_token in item_value for item_value in item_tokens) for search_token in search_tokens):
            # if all(any(search_token in item_value for item_value in item_tokens) for search_token in search_tokens):
                # print("vale is: ", item_tokens)
                self.treeview.insert("", "end", iid=item[0], values=item[1:])
        
        
        self.treeview.column('#1', anchor="e", width=100)

if __name__ == "__main__":
    app = FilterableTreeviewApp()
    app.mainloop()

    # def filter_treeview_strict(self, *args):
    #     search_term = self.search_var.get().lower()

    #     # Clear the treeview
    #     for item in self.treeview.get_children():
    #         self.treeview.delete(item)

    #     # Re-insert items that match the search term
    #     for item in self.all_items:
    #         item_values = [value.lower() for value in item]

    #         # Tokenize the values by splitting on commas and spaces
    #         item_tokens = []
    #         for value in item_values:
    #             tokens = value.replace(',', '').split()
    #             item_tokens.extend(tokens)

    #         # If any of the tokens match the search_term, insert the item
    #         if any(search_term in token for token in item_tokens):
    #             self.treeview.insert("", "end", values=item)


    # def filter_treeview_base(self, *args):
    #     search_term = self.search_var.get().lower()

    #     # Clear the treeview
    #     for item in self.treeview.get_children():
    #         self.treeview.delete(item)

    #     # Re-insert items that match the search term
    #     for item in self.all_items:
    #         item_values = [value.lower() for value in item]

    #         # If any of the item_values match the search_term, insert the item
    #         if any(search_term in value for value in item_values):
    #             self.treeview.insert("", "end", values=item)
