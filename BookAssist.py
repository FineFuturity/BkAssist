# import tkinter as tk
# from tkinter import ttk
# from tkinter import filedialog
# import pandas as pd
# import chardet as cd
# import os

from header import *

filetypes = [
               ("Excel Workbook and .CSV files", "*.csv;*.xlsx;*.xls"),
               ("Comma-separated Values file", "*.csv"),
               ("Excel Workbook file", "*.xlsx;*.xls")
            ]

cur_file = None

# Create a root window
root = tk.Tk()
root.title(title)
root.geometry("800x600")

 # Create a menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)

def file_frm_usr():
    # Prompt the user to select a file
    return filedialog.askopenfilename(parent=root,
        title="Select a file",
        filetypes=filetypes
    )

def on_double_click(event, tree):
    # Get the selected item
    # item_id = tree.focus()
    # print("iid:", item_id)

    # Get the item that was clicked
    item = tree.selection()[0]

    # Get the values of the selected row
    values = tree.item(item)['values']

    # Create a Toplevel window
    top = tk.Toplevel(root)
    try:
        top_title_info = values[0].upper()
    except:
        top_title_info = str(values[0])

    top.title("Information for " + top_title_info )
    top.geometry("400x400")
    # top.resizable(0,0)

    # Create a Treeview widget in the Toplevel window
    top_tree = ttk.Treeview(top, columns=('Attributes', 'Data'))
    top_tree.pack(fill='both', expand=True)

    #prevent the empty iid column from appearing
    top_tree["show"] = "headings"

    # create and format the two columns for population of the selected row data
    attrhdr = ''
    if dev:
        attrhdr = 'Attributes'
    top_tree.heading(attrhdr, text='Attributes', anchor="e")
    top_tree.heading('Data', text='Data', anchor="w")
    top_tree.column('Attributes', anchor="e")
    top_tree.column('Data', anchor="w")

    for idx, val in enumerate(values):
        col_name = tree.heading(idx)['text']
        top_tree.insert('', 'end', text='', values=(col_name, val))

# Define a function to handle double-click events on Treeview items
def on_double_click_old(event, tree):
    # Get the selected item
    # item_id = tree.focus()
    # print("iid:", item_id)

    # Get the item that was clicked
    item = tree.selection()[0]

    # Get the values of the selected row
    values = tree.item(item)['values']

    # Create a Toplevel window
    top = tk.Toplevel(root)
    top.title("Information for " + str(values[0]) )
    top.geometry("400x400")
    # top.resizable(0,0)

    # Create a Treeview widget in the Toplevel window
    top_tree = ttk.Treeview(top, columns=('Attributes', 'Data'), style="mystyle.Treeview")
    top_tree.pack(fill='both', expand=True)

    # Set column headings
    # top_tree.heading('#0', text='', anchor='center')
    # top_tree['show'] = 'tree'
    #prevent the empty iid column from appearing
    top_tree["show"] = "headings"
    top_tree.heading('Attributes', text='', anchor="center")
    top_tree.heading('Data', text='Data', anchor="w")
    top_tree.column('Attributes', anchor="center")
    top_tree.column('Data', anchor="w")

    # Populate the treeview with the selected row data
    for idx, val in enumerate(values):
        col_name = tree.heading(idx)['text']
        top_tree.insert('', 'end', text='', values=(col_name, val))

def sort_treeview(treeview, col, descending=False):
    # Sort the data by the given column
    treeview.sort(column=col, descending=descending)

def is_not_ascii(string):
    return string is not None and any([ord(s) >= 128 for s in string])

def det_csv_enc(file_path):
    # Open the file in binary mode and read a small amount of the contents
    with open(file_path, "rb") as f:
        contents = f.read(1000)

    # Detect the encoding of the contents using chardet
    result = cd.detect(contents)
    encoding = result["encoding"]
    print(encoding)

    return encoding

def update_dataframe(event, tree, df):
    # Get all items in the Treeview
    items = tree.get_children()

    # Create a list of all item data
    data = []
    for item in items:
        data.append(tree.item(item)['values'])

    # Convert data to a DataFrame and update the global variable
    df = pd.DataFrame(data, columns=tree['columns'])

def update_treeview(tree):
    # Clear the current Treeview items
    tree.delete(*tree.get_children())

    # Add the updated DataFrame to the Treeview
    for index, row in df.iterrows():
        tree.insert("", index, values=tuple(row))

def update_prog_data(tree, df):
    update_dataframe(tree)
    update_treeview(tree)

file_path = file_frm_usr()

data = None

# Check the file extension to determine the file type
curr_file, file_extension = os.path.splitext(file_path)
file_name = file_path.split("/")[-1]
print(curr_file)  # Output: /path/to/myfile
print(file_extension)

ok = False
if file_extension == ".csv":
    # Read data from CSV file into a pandas DataFrame
    encoding = det_csv_enc(file_path)
    try:
        data = pd.read_csv(file_path, encoding=encoding, dtype=str)
        data['row_id'] = data.index
        ok = True
    except:
        cur_file = None
        tk.messagebox.showerror(f"Error Loading file: {file_name}{file_extension}", f"Unable to read file with {encoding} encoding. Please ")
elif file_extension in (".xlsx", ".xls"):
    # Read data from Excel file into a pandas DataFrame
    data = pd.read_excel(file_path, dtype=str)
    # data['row_id'] = data.index
    ok = True
else:
    # Show an error message if the file type is not supported
    tk.messagebox.showerror("Error", "Unsupported file type")
    exit()

if ok:
    # Replace NaN values with an empty string
    data.fillna('-', inplace=True)
    print(data)


    # Create a Treeview widget
    tree = ttk.Treeview(root)

    tree["columns"] = tuple(data.columns)

    # Create a horizontal scrollbar
    h_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)

    # Create a vertical scrollbar
    v_scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)


    # Set the column headings
    for col in data.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    # Add data to the Treeview
    for idx, row in data.iterrows():
        iid = str(idx)
        tree.insert("", "end", iid=iid, values=tuple(row))

    #prevent the empty iid column from appearing
    # if not dev:
    tree["show"] = "headings"
    tree.heading('#1', anchor="e")
    tree.column('#1', anchor="e")

    # Configure the Treeview to use the scrollbars
    tree.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)

    # Pack the Treeview widget
    h_scrollbar.pack(side="bottom", fill="x")
    v_scrollbar.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    # Bind the Treeview widget to the double-click event handler
    tree.bind("<Double-1>", lambda event: on_double_click(event, tree))

# Start the main event loop
root.mainloop()

# # Create a file menu
# file_menu = tk.Menu(menubar, tearoff=False)
# menubar.add_cascade(label="File", menu=file_menu)
# file_menu.add_command(label="Open", command=file_from_usr)

# # ------ FILTER AS YOU SEARCH END HERE ------

# # Create a search frame
# search_frame = ttk.Frame(root)
# search_frame.pack(side=tk.TOP, fill=tk.X)

# # Create a search label and entry
# search_label = ttk.Label(search_frame, text="Search:")
# search_label.pack(side=tk.LEFT, padx=5, pady=5)
# search_entry = ttk.Entry(search_frame)
# search_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
# search_entry.bind("<KeyRelease>", lambda event: filter_data)

# def filter_data(event):
#         # Get the search query
#         query = search_entry.get().lower()

#         # Clear the existing treeview
#         tree.delete(*tree.get_children())
#         # Add the columns to the treeview
#         columns = list(df.columns)
#         tree.config(columns=columns)
#         tree["show"] = "headings"
#         for column in columns:
#             tree.heading(column, text=column)

#         # Filter the rows based on the search query
#         filtered_df = df[df.apply(lambda row: any(str(cell).lower().startswith(query) for cell in row), axis=1)]
#         for row in filtered_df.itertuples():
#             row_values = list(row)[1:]
#             tree.insert("", "end", values=row_values)

# ------ FILTER AS YOU SEARCH END HERE ------


# Define the columns
# data_columns =  ["row_id"] + list(data.columns)
# tree["columns"] = data_columns

# def get_file():
#     filetypes = ()
#     for description, ftype in sup_types:
#         filetypes.append(ftype)


#     file_path = filedialog.askopenfilename(
#         title="Select a file",
#         filetypes=(
#             ("CSV and Excel files", "*.csv;*.xlsx;*.xls"),
#             ("CSV files", "*.csv"),
#             ("Excel files", "*.xlsx;*.xls")
#         )
#     )