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
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo, showerror

from pathlib import Path
from configuration.configuration import DATA_PATH


class ControlFrame(tk.Frame):
    def __init__(self, master):

        super().__init__(master)
        self.master = master
        master.wm_title("Word genders")
        master.geometry("300x500")
        master.resizable(False, False)
        master.protocol("WM_DELETE_WINDOW", master.close_window)

        # main titel
        self.frame_confi = tk.Frame(self)
        self.frame_confi.pack(side="top", padx="5", pady="5")
        tk.Label(
            self.frame_confi, text="Configuration", font="Verdana 14 bold", fg="black"
        ).pack(side="top", fill="x", pady=10)

        # Training language
        self.frame_training_language = tk.Frame(self)
        self.frame_training_language.pack(side="top", padx="5", pady="5", fill="x")
        tk.Frame(self.frame_training_language, height=2, bd=1, relief=tk.SUNKEN).pack(
            fill=tk.X, padx=5, pady=5
        )
        tk.Label(
            self.frame_training_language,
            text="Choose training language",
            font="Verdana 10 bold",
            fg="black",
        ).pack(side="top", fill="x", pady=10)
        self.selected_language = tk.StringVar()
        self.selected_language.set(self.master.configuration.language)
        tk.Radiobutton(
            self.frame_training_language,
            text="German",
            value="de",
            variable=self.selected_language,
            command=self.select_training_language,
        ).pack()
        tk.Radiobutton(
            self.frame_training_language,
            text="Russian",
            value="ru",
            variable=self.selected_language,
            command=self.select_training_language,
        ).pack()

        # Load dictionary
        self.frame_load_dic = tk.Frame(self)
        self.frame_load_dic.pack(side="top", padx="5", pady="5", fill="x")
        tk.Frame(self.frame_load_dic, height=2, bd=1, relief=tk.SUNKEN).pack(
            fill=tk.X, padx=5, pady=5
        )
        tk.Label(
            self.frame_load_dic,
            text="Load dictionary",
            font="Verdana 10 bold",
            fg="black",
        ).pack(side="top", fill="x", pady=10)
        self.active_dictionary = tk.Label(
            self.frame_load_dic,
            text=self.master.dictionary.name,
            font="Purisa 9 bold",
            fg="green",
        )
        self.active_dictionary.pack(side="top", fill="x", pady=10)
        ttk.Button(
            self.frame_load_dic, width=15, text="Load file", command=self.select_file
        ).pack(padx="3", side=tk.LEFT)
        ttk.Button(
            self.frame_load_dic, width=15, text="Dict info", command=self.select_file
        ).pack(padx="3", side=tk.LEFT)

        # Tools
        self.frame_tools = tk.Frame(self)
        self.frame_tools.pack(side="top", padx="5", pady="5", fill="x")
        tk.Frame(self.frame_tools, height=2, bd=1, relief=tk.SUNKEN).pack(
            fill=tk.X, padx=5, pady=5
        )
        tk.Label(
            self.frame_tools, text="Tools", font="Verdana 12 bold", fg="black"
        ).pack(side="top", fill="x", pady=10)
        tk.Button(
            self.frame_tools,
            width=15,
            text="Nouns genders",
            command=self.switch_nouns_frame,
        ).pack(padx=5, pady=5)
        tk.Button(
            self.frame_tools,
            width=15,
            text="Meanings",
            command=lambda: master.switch_frame("nouns"),
        ).pack(padx=5, pady=5)
        tk.Button(
            self.frame_tools,
            width=15,
            text="Manage words",
            command=lambda: master.switch_frame("manage_words"),
        ).pack(padx=5, pady=5)

    def switch_nouns_frame(self):
        if self.master.dictionary.kind == "nouns":
            self.master.switch_frame("nouns")
        else:
            showerror(
                title="Wrong dictionary",
                message=f"The dictionary {self.master.dictionary.name} is not for nouns.",
            )

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
