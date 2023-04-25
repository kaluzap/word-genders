"""
Control Frame

This Frame sets the following parameters:
1. the system langauge
2. the training languaje
3. the dictionary

In addiotion it loads the tools:
1. nouns
2. meanings
3. load dictionary
4. add or remove words to/from the dictionary
"""

import tkinter as tk
#from tkinter import ttk
from tkinter.messagebox import showerror


from util.nouns import ConverterFrame, TemperatureConverter


class Nouns(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        container.title("NOUNS")

class ControlFrame(tk.Frame):
    def __init__(self, container):

        super().__init__(container)
        self.container = container
        

        # initialize frames
        self.frames = {}
        self.frames["nouns"] = ConverterFrame(
            container,
            'Fahrenheit',
            TemperatureConverter.fahrenheit_to_celsius)
        self.frames["meanings"] = Nouns(self.container)
        


        # subframe for language
        self.frame_language = tk.Frame(self.container)
        self.frame_language.pack(side="top", padx="5", pady="5")

        self.selected_language = tk.StringVar()
        self.selected_language.set("ge")

        self.label_language = tk.Label(master=self.frame_language, text=f"Languages ({self.selected_language.get()})")
        self.label_language.pack(side=tk.TOP, padx="5", pady="5")
        
        # radio buttons
        tk.Radiobutton(
            self.container,
            text='German',
            value="ge",
            variable=self.selected_language,
            command=self.update_label_language).pack(side=tk.TOP, padx="5", pady="5")

        tk.Radiobutton(
            self.container,
            text='Russian',
            value="ru",
            variable=self.selected_language,
            command=self.update_label_language).pack(side=tk.TOP, padx="5", pady="5")
        
        
        self.mButton = tk.Button(
            master=self.frame_language,
            command=self.change_frame,
            text="Nouns",
        )
        self.mButton.pack(side=tk.BOTTOM, padx="5", pady="5")
        

    def update_label_language(self):
        text=f"Languages ({self.selected_language.get()})"
        self.label_language.config(text = text)
        
    def change_frame(self):
        frame = self.frames["nouns"]
        frame.tkraise()
