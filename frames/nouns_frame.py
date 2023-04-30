import argparse
import pandas as pd
from numpy import random
from util import util
from tkinter import (
    Tk,
    NORMAL,
    DISABLED,
    LEFT,
    Frame,
    IntVar,
    Label,
    Button,
    Checkbutton,
    TOP,
)
from PIL import ImageTk
import json


class NounsFrame(Frame):
    def __init__(self, master=None):
        # Windows
        Frame.__init__(self, master)
        self.master = master
        master.wm_title("Noun genders")
        master.geometry("550x550")
        master.resizable(False, False)

        # state variables
        self.active_word = ""
        self.active_case = ""
        self.text_to_speak = ""
        self.count_good = 0
        self.count_total_clicks = 0
        self.count_total_words = 0
        self.already_tested = False
        self.allow_repetitions = IntVar()
        self.allow_repetitions.set(1)
        self.my_success = util.SuccessStreak()
        self.create_figure()
        # starting a word
        self.set_new_active_word_and_case()

        # subframe for texts
        self.frame_texts = Frame(self)
        self.frame_texts.pack(side="top", padx="5", pady="5")

        self.label_status = Label(
            master=self.frame_texts,
            **self.master.configuration.sys_dict["label_properties"]["label_status"],
        )
        self.label_status.pack(side=TOP, padx="5", pady="5")

        self.label_word = Label(
            master=self.frame_texts,
            **self.master.configuration.sys_dict["label_properties"]["label_word"],
        )
        self.label_word.pack(side=TOP, padx="5", pady="5")

        self.label_translation = Label(
            master=self.frame_texts,
            **self.master.configuration.sys_dict["label_properties"][
                "label_translation"
            ],
        )
        self.label_translation.pack(side=TOP, padx="5", pady="5")

        self.label_full_data = Label(
            master=self.frame_texts,
            **self.master.configuration.sys_dict["label_properties"]["label_full_data"],
        )
        self.label_full_data.pack(side=TOP, padx="5", pady="5")

        self.label_points = Label(
            master=self.frame_texts,
            **self.master.configuration.sys_dict["label_properties"]["label_points"],
        )
        self.label_points.pack(side=TOP, padx="5", pady="5")

        render = ImageTk.PhotoImage(self.my_success.last_success_streak_img)
        self.img = Label(master=self.frame_texts, image=render)
        self.img.image = render
        self.img.pack(side=TOP, padx="5", pady="5")

        # subframe for article buttons
        self.frame_button_articles = Frame(self)
        self.frame_button_articles.pack(side="top", padx="5", pady="5")

        self.mButton = Button(
            master=self.frame_button_articles,
            command=self.clickmButton,
            **self.master.configuration.sys_dict["button_properties"]["article_m"],
        )
        self.mButton.pack(side=LEFT, padx="5")

        self.fButton = Button(
            master=self.frame_button_articles,
            command=self.clickfButton,
            **self.master.configuration.sys_dict["button_properties"]["article_f"],
        )
        self.fButton.pack(side=LEFT, padx="5")

        self.nButton = Button(
            master=self.frame_button_articles,
            command=self.clicknButton,
            **self.master.configuration.sys_dict["button_properties"]["article_n"],
        )
        self.nButton.pack(side=LEFT, padx="5")

        self.pButton = Button(
            master=self.frame_button_articles,
            command=self.clickpButton,
            **self.master.configuration.sys_dict["button_properties"]["article_p"],
        )
        self.pButton.pack(side=LEFT, padx="5")

        # subframe for functions buttons
        self.frame_button_functions = Frame(self)
        self.frame_button_functions.pack(side="top", padx="5", pady="5")

        self.CheckbuttonRepetitions = Checkbutton(
            master=self.frame_button_functions,
            text=self.master.configuration.sys_dict["checkbuttons"]["repetitions"],
            variable=self.allow_repetitions,
        )
        self.CheckbuttonRepetitions.pack(side=LEFT, padx="5")

        self.dataButton = Button(
            master=self.frame_button_functions,
            command=self.clickDataButton,
            **self.master.configuration.sys_dict["button_properties"]["data"],
        )
        self.dataButton.pack(side=LEFT, padx="5")

        self.soundButton = Button(
            master=self.frame_button_functions,
            command=self.clickSoundButton,
            **self.master.configuration.sys_dict["button_properties"]["sound"],
        )
        self.soundButton.pack(side=LEFT, padx="5")

        self.nextButton = Button(
            master=self.frame_button_functions,
            command=self.clickNextButton,
            state=DISABLED,
            **self.master.configuration.sys_dict["button_properties"]["next"],
        )
        self.nextButton.pack(side=LEFT, padx="5")

        Button(
            self, text="Return to main page", command=self.return_to_main_page
        ).pack()

    def return_to_main_page(self):
        self.master.dictionary.save_dictionary()
        self.master.switch_frame("control")

    def set_new_active_word_and_case(self):
        try:
            if self.allow_repetitions.get():
                indexes = [x for x in range(0, self.master.dictionary.data.shape[0])]
                total = self.master.dictionary.data["mistakes"].sum()
                if total == 0:
                    self.master.dictionary.data[
                        "p"
                    ] = self.master.dictionary.data.apply(
                        lambda row: 1 / len(indexes), axis=1
                    )
                else:
                    self.master.dictionary.data[
                        "p"
                    ] = self.master.dictionary.data.apply(
                        lambda row: row["mistakes"] / total, axis=1
                    )
                the_index = random.choice(
                    indexes, 1, p=self.master.dictionary.data["p"].to_list()
                )[0]
                # print(self.master.dictionary.data['p'].to_list())
                # print(f"the_index = {the_index}")
                df_sample = self.master.dictionary.data[
                    self.master.dictionary.data.index == the_index
                ]
            else:
                df_sample = self.master.dictionary.data[
                    self.master.dictionary.data["active"]
                ].sample()
            # print(df_sample.head())
        except ValueError as err:
            print(f"No hay mas palabras {err}!!!")
            return self.active_word, self.active_case

        self.active_word = df_sample.iloc[0].to_dict()
        self.active_word["index"] = df_sample.index[0]
        self.master.dictionary.data.at[self.active_word["index"], "active"] = False
        if not self.allow_repetitions.get():
            print(
                f"There are {self.master.dictionary.data[self.master.dictionary.data['active']==True].shape[0]} words left."
            )

        self.active_case = random_case()
        if (self.active_word["plural"] == "-") and (self.active_case == "p"):
            self.active_case = "s"
        if self.active_word["singular"] == self.active_word["plural"]:
            self.active_case = "sp"
        if self.active_word["singular"] == "-":
            self.active_case = "p"

        if self.active_case == "s":
            self.text_to_speak = self.active_word["singular"]
        else:
            self.text_to_speak = self.active_word["plural"]

        self.master.configuration.sys_dict["label_properties"]["label_status"][
            "text"
        ] = " "
        if self.active_case == "s":
            self.master.configuration.sys_dict["label_properties"]["label_word"][
                "text"
            ] = self.active_word["singular"]
        else:
            self.master.configuration.sys_dict["label_properties"]["label_word"][
                "text"
            ] = self.active_word["plural"]
        self.master.configuration.sys_dict["label_properties"]["label_translation"][
            "text"
        ] = f"({self.active_word['translation']})"
        self.master.configuration.sys_dict["label_properties"]["label_full_data"][
            "text"
        ] = " "
        self.master.configuration.sys_dict["label_properties"]["label_points"][
            "text"
        ] = self.count_statistics()

    def count_statistics(self):
        line = ""
        if not self.count_total_words:
            ratio_success = 0
        else:
            ratio_success = self.count_good / self.count_total_words
        line = f"{self.master.configuration.sys_dict['statistics']['success_rate']}: {self.count_good}/{self.count_total_words} = {ratio_success:.5f}"
        if ratio_success > 0.9:
            line += "    :)\n"
        else:
            line += "    :(\n"
        if not self.count_total_clicks:
            ratio_attempts = 0
        else:
            ratio_attempts = self.count_good / self.count_total_clicks
        line += f"{self.master.configuration.sys_dict['statistics']['attempts_rate']}: {self.count_good}/{self.count_total_clicks} = {ratio_attempts:.5f}"
        if ratio_attempts > 0.9:
            line += "    :)\n"
        else:
            line += "    :(\n"
        line += f"{self.master.configuration.sys_dict['statistics']['success_streak']}: {self.my_success.success_streak} ({self.my_success.success_streak_record})"
        return line

    def update_labels(self):
        self.label_status["text"] = self.master.configuration.sys_dict[
            "label_properties"
        ]["label_status"]["text"]
        self.label_word["text"] = self.master.configuration.sys_dict[
            "label_properties"
        ]["label_word"]["text"]
        self.label_word["fg"] = self.master.configuration.sys_dict["label_properties"][
            "label_word"
        ]["fg"]
        self.label_translation["text"] = self.master.configuration.sys_dict[
            "label_properties"
        ]["label_translation"]["text"]
        self.label_full_data["text"] = self.master.configuration.sys_dict[
            "label_properties"
        ]["label_full_data"]["text"]
        self.label_full_data["fg"] = self.master.configuration.sys_dict[
            "label_properties"
        ]["label_full_data"]["fg"]
        self.label_points["text"] = self.master.configuration.sys_dict[
            "label_properties"
        ]["label_points"]["text"]

        img2 = ImageTk.PhotoImage(self.my_success.last_success_streak_img)
        self.img.configure(image=img2)
        self.img.image = img2

    def disable_next_button(self):
        self.nextButton["state"] = DISABLED

    def enable_next_button(self):
        self.nextButton["state"] = NORMAL

    def disable_article_buttons(self):
        self.mButton["state"] = DISABLED
        self.fButton["state"] = DISABLED
        self.nButton["state"] = DISABLED
        self.pButton["state"] = DISABLED

    def enable_article_buttons(self):
        self.mButton["state"] = NORMAL
        self.fButton["state"] = NORMAL
        self.nButton["state"] = NORMAL
        self.pButton["state"] = NORMAL

    def create_string_result(self):
        text = ""
        if self.active_word["singular"] == "-":
            text += f"[{self.master.configuration.sys_dict['missing_gender']['without_singular']}], "
        else:
            if "m" in self.active_word["gender"]:
                text += self.master.configuration.sys_dict["article_texts"]["m"] + " "
            if "f" in self.active_word["gender"]:
                text += self.master.configuration.sys_dict["article_texts"]["f"] + " "
            if "n" in self.active_word["gender"]:
                text += self.master.configuration.sys_dict["article_texts"]["n"] + " "
            text += self.active_word["singular"] + ", "

        if self.active_word["plural"] == "-":
            text += f"[{self.master.configuration.sys_dict['missing_gender']['without_plural']}]"
        else:
            text += f"{self.master.configuration.sys_dict['article_texts']['p']} {self.active_word['plural']}"
        self.text_to_speak = text
        return text

    def run_button_gender(self, gender):
        self.count_total_clicks += 1
        if self.test_word(gender):
            self.my_success.add_new_sucess()
            if not self.already_tested:
                self.count_good += 1
                self.master.dictionary.data.at[
                    self.active_word["index"], "mistakes"
                ] -= 1
                if (
                    self.master.dictionary.data.at[
                        self.active_word["index"], "mistakes"
                    ]
                    < 1
                ):
                    self.master.dictionary.data.at[
                        self.active_word["index"], "mistakes"
                    ] = 1
            else:
                self.master.dictionary.data.at[
                    self.active_word["index"], "active"
                ] = True
            self.disable_article_buttons()
            self.enable_next_button()
            self.count_total_words += 1
            self.master.configuration.sys_dict["label_properties"]["label_status"][
                "text"
            ] = self.master.configuration.sys_dict["message_status"]["correct"]
            if self.my_success.is_record:
                self.master.configuration.sys_dict["label_properties"]["label_status"][
                    "text"
                ] = (
                    self.master.configuration.sys_dict["message_status"]["correct"]
                    + f"   {self.master.configuration.sys_dict['message_status']['record']}"
                )
            self.master.configuration.sys_dict["label_properties"]["label_word"][
                "fg"
            ] = self.master.configuration.sys_dict["gender_color"][gender]
            self.master.configuration.sys_dict["label_properties"]["label_full_data"][
                "text"
            ] = self.create_string_result()
            self.master.configuration.sys_dict["label_properties"]["label_full_data"][
                "fg"
            ] = self.master.configuration.sys_dict["gender_color"][gender]

        else:
            self.master.configuration.sys_dict["label_properties"]["label_status"][
                "text"
            ] = self.master.configuration.sys_dict["message_status"]["wrong"]
            self.my_success.stop_success_streak()
            self.master.dictionary.data.at[self.active_word["index"], "mistakes"] += 1

        self.create_figure()
        self.master.configuration.sys_dict["label_properties"]["label_points"][
            "text"
        ] = self.count_statistics()
        self.already_tested = True
        self.update_labels()

    def create_figure(self):
        self.my_success.make_success_streak_figure(
            xlabel=self.master.configuration.sys_dict["figure"]["xlabel"],
            ylabel=self.master.configuration.sys_dict["figure"]["ylabel"],
        )

    def test_word(self, gender):
        if ("s" in self.active_case) and (gender in self.active_word["gender"]):
            return True
        if gender in self.active_case:
            return True
        return False

    def clickmButton(self):
        self.run_button_gender("m")

    def clickfButton(self):
        self.run_button_gender("f")

    def clicknButton(self):
        self.run_button_gender("n")

    def clickpButton(self):
        self.run_button_gender("p")

    def clickDataButton(self):
        self.master.dictionary.make_all_active()

    def clickSoundButton(self):
        self.text_to_speak = self.text_to_speak.replace(
            f"[{self.master.configuration.sys_dict['missing_gender']['without_singular']}], ",
            "",
        )
        self.text_to_speak = self.text_to_speak.replace(
            f"[{self.master.configuration.sys_dict['missing_gender']['without_plural']}]",
            "",
        )
        util.play_string(
            text=self.text_to_speak, language=self.master.configuration.language
        )

    def clickNextButton(self):
        self.set_new_active_word_and_case()
        self.master.configuration.sys_dict["label_properties"]["label_word"][
            "fg"
        ] = "black"
        self.update_labels()
        self.enable_article_buttons()
        self.disable_next_button()
        self.already_tested = False


def random_case() -> str:
    x = random.rand()
    if x < 0.75:
        return "s"
    return "p"
