"""
Control Frame

This Frame sets the following parameters:
1. the training languaje
2. the dictionary

In addiotion it loads the tools:
1. nouns
2. meanings
3. load dictionary
4. add or remove words to/from the dictionary
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showinfo

from pathlib import Path
from configuration.configuration import DATA_PATH


class ControlFrame(tk.Frame):
    def __init__(self, master):

        super().__init__(master)
        self.master = master
        master.wm_title("WORDS!")
        master.geometry("300x440")

        tk.Label(self, text="Configuration", font="Verdana 14 bold", fg="black").pack(
            side="top", fill="x", pady=10
        )
        tk.Frame(self, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=5)

        # Training language
        tk.Label(
            self, text="Choose training language", font="Verdana 10 bold", fg="black"
        ).pack(side="top", fill="x", pady=10)
        self.selected_language = tk.StringVar()
        self.selected_language.set(self.master.configuration.language)
        tk.Radiobutton(
            self, text="German", value="de", variable=self.selected_language, command=self.select_training_language
        ).pack()
        tk.Radiobutton(
            self, text="Russian", value="ru", variable=self.selected_language, command=self.select_training_language
        ).pack()
        tk.Frame(self, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=5)

        # Load dictionary
        tk.Label(self, text="Load dictionary", font="Verdana 10 bold", fg="black").pack(
            side="top", fill="x", pady=10
        )
        self.active_dictionary = tk.Label(
            self, text=self.master.dictionary.name, font="Purisa 9 bold", fg="green"
        )
        self.active_dictionary.pack(side="top", fill="x", pady=10)
        ttk.Button(self, width=15, text="Open a File", command=self.select_file).pack(
            expand=True
        )
        tk.Frame(self, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=5)

        # Tools
        tk.Label(self, text="Tools", font="Verdana 12 bold", fg="black").pack(
            side="top", fill="x", pady=10
        )
        tk.Button(
            self,
            width=15,
            text="Nouns genders",
            command=lambda: master.switch_frame("nouns"),
        ).pack(expand=True)
        tk.Button(
            self,
            width=15,
            text="Meanings",
            command=lambda: master.switch_frame("nouns"),
        ).pack(expand=True)
        tk.Button(
            self,
            width=15,
            text="Add or delete words",
            command=lambda: master.switch_frame("nouns"),
        ).pack(expand=True)

    def select_training_language(self):
        self.master.configuration.load_configuration(self.selected_language.get())
        
    def select_file(self):
        filetypes = (("Data files", "*.csv"), ("All files", "*.*"))

        filename = filedialog.askopenfilename(
            title="Open a file", initialdir=DATA_PATH, filetypes=filetypes
        )

        if not filename:
            message = "No file"
        else:
            self.master.dictionary.load_dictionary(filename)
            message = f"File: {Path(filename).name}\nWords: {self.master.dictionary.data.shape[0]}"
            self.active_dictionary["text"] = f"{Path(filename).name}"
            showinfo(title="Selected File", message=message)
