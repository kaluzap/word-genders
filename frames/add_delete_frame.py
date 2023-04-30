import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showinfo, showerror

from pathlib import Path
from configuration.configuration import DATA_PATH


class AddDeleteFrame(tk.Frame):
    def __init__(self, master):

        super().__init__(master)
        self.master = master
        master.wm_title("Add/Delete words")
        master.geometry("300x440")
        master.resizable(False, False)
        
        
        
        self.my_entry = tk.Entry(self, width = 20)
        self.my_entry.insert(0,'Singular')
        self.my_entry.pack(padx = 5, pady = 5)
