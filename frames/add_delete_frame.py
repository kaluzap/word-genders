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
        master.wm_title("Manage words")
        master.geometry("500x330")
        master.resizable(False, False)
        
        # subframe for adding words
        self.frame_add = tk.Frame(self)
        self.frame_add.pack(side="top", padx="5", pady="5")
        self.label_add = tk.Label(self.frame_add, text="Manage words", font="Verdana 14 bold", fg="black").pack(side=tk.TOP, padx="5", pady="5")
        
        # subframe singular
        self.frame_singular = tk.Frame(self)
        self.frame_singular.pack(side="top", padx="5", pady="5")
        tk.Label(self.frame_singular, text="Singular:   ", font="Verdana 10", fg="black").pack(side=tk.LEFT, padx="5", pady="5")
        self.my_entry_singular = tk.Entry(self.frame_singular, width = 50)
        self.my_entry_singular.pack(side=tk.LEFT, padx="5")
        
        # subframe plural
        self.frame_plural = tk.Frame(self)
        self.frame_plural.pack(side="top", padx="5", pady="5")
        tk.Label(self.frame_plural, text="Plural:       ", font="Verdana 10", fg="black").pack(side=tk.LEFT, padx="5", pady="5")
        self.my_entry_plural = tk.Entry(self.frame_plural, width = 50)
        self.my_entry_plural.pack(side=tk.LEFT, padx="5")
        
        # subframe meanings
        self.frame_meanings = tk.Frame(self)
        self.frame_meanings.pack(side="top", padx="5", pady="5")
        tk.Label(self.frame_meanings, text="Meanings:", font="Verdana 10", fg="black").pack(side=tk.LEFT, padx="5", pady="5")
        self.my_entry_meanings = tk.Entry(self.frame_meanings, width = 50)
        self.my_entry_meanings.pack(side=tk.LEFT, padx="5")
        
        # subframe gender
        self.frame_gender = tk.Frame(self)
        self.frame_gender.pack(side="top", padx="5", pady="5")
        self.selected_gender = tk.StringVar()
        self.selected_gender.set("")
        tk.Radiobutton(
            self.frame_gender, text="Masculine", value="m", variable=self.selected_gender, command=self.switch_gender
        ).pack(side=tk.LEFT, padx="5")
        tk.Radiobutton(
            self.frame_gender, text=", Feminine", value="f", variable=self.selected_gender, command=self.switch_gender
        ).pack(side=tk.LEFT, padx="5")
        tk.Radiobutton(
            self.frame_gender, text="Neuter", value="n", variable=self.selected_gender, command=self.switch_gender
        ).pack(side=tk.LEFT, padx="5")
        
        tk.Frame(self, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=5)
        
        # subframe actions
        self.frame_actions = tk.Frame(self)
        self.frame_actions.pack(side="top", padx="5", pady="5")
        tk.Button(
            self.frame_actions,
            width=10,
            text="Add",
            command=self.switch_gender,
        ).pack(side=tk.LEFT, padx="5")
        tk.Button(
            self.frame_actions,
            width=10,
            text="Find",
            command=self.switch_gender,
        ).pack(side=tk.LEFT, padx="5")
        tk.Button(
            self.frame_actions,
            width=10,
            text="Delete",
            command=self.switch_gender,
        ).pack(side=tk.LEFT, padx="5")
        tk.Button(
            self.frame_actions,
            width=10,
            text="clean",
            command=self.switch_gender,
        ).pack(side=tk.LEFT, padx="5")
        
        
        tk.Frame(self, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=5)
        
        # subframe actions
        self.frame_exit = tk.Frame(self)
        self.frame_exit.pack(side="top", padx="5", pady="5")
        tk.Button(
            self.frame_exit, text="Return to main page", command=self.return_to_main_page
        ).pack(side=tk.LEFT, padx="5")

    def return_to_main_page(self):
        #self.master.dictionary.save_dictionary()
        self.master.switch_frame("control")
        
        
    def switch_gender(self):
        print(self.selected_gender.get())
        
        
        """
        tk.Button(
            frame_gender,
            width=15,
            text="Masulin",
            command=self.switch_gender,
        ).pack(side=tk.LEFT, padx="5")
        
        """
        
        
