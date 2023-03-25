import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pyodbc
from PIL import ImageTk, Image
import pandas as pd
import openpyxl
import chardet as cd
import os
import csv
from tkinter.messagebox import askyesno

def _convert_stringval(value):
    """Converts a value to, hopefully, a more appropriate Python object."""
    if hasattr(value, 'typename'):
        value = str(value)
        try:
            value = int(value)
        except (ValueError, TypeError):
            pass
    return value

ttk._convert_stringval = _convert_stringval
name = "Bookkeeping Assistant"
ver = "1.0"
phase = "alpha"
branch = "dev.main"
build = ver + ".1000.0324-0742"
client_env = "DEVELOPER" #dev, client-test, client-prod
full_build_tag = name + "\nVer. " + ver + "." + build + "." + branch + " (" + phase + ")\nFor testing purposes only."
dev = True
authd = True

# Window Title Strings
title = name
brc_str = " ( ver. " + build + ", " + branch + " branch )"
if dev:
    title = title + brc_str
