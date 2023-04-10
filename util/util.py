import argparse
from gtts import gTTS
from io import BytesIO
from pygame import mixer
import matplotlib.pyplot as plt
from PIL import Image
import time

        
class SuccessStreak:
    def __init__(self):
        # list of succes streaks
        self.success_streak_history = []
        # actual success streak
        self.success_streak = 0
        # success streak record
        self.success_streak_record = 0
        # imagen of last imagen
        self.last_success_streak_img = None
        # is record
        self.is_record = False

    def add_new_sucess(self):
        self.success_streak += 1
        if self.success_streak > self.success_streak_record:
            self.is_record = True
            self.success_streak_record = self.success_streak
        else:
            self.is_record = False

    def stop_success_streak(self):
        self.success_streak_history.append(self.success_streak)
        self.success_streak = 0
        self.success_streak_record = max(self.success_streak_history)

    def make_success_streak_figure(self, xlabel: str, ylabel: str):  # -> Image.Image:
        plt.rcParams["figure.figsize"] = (4.5, 1.75)
        plt.ylabel(xlabel, fontsize=8)
        plt.xlabel(ylabel, fontsize=8)
        plt.rc("xtick", labelsize=6)
        plt.rc("ytick", labelsize=6)
        plt.xticks(range(0, self.success_streak_record + 1))

        if len(self.success_streak_history) != 0:
            plt.yticks(range(0, max(self.success_streak_history) + 1))
        else:
            plt.yticks(range(0, 1))

        plt.hist(
            self.success_streak_history + [self.success_streak],
            bins=self.success_streak_record + 1,
            range=(-0.5, self.success_streak_record + 0.5),
            color=(0.59, 0.59, 0.59),
        )
        plt.grid()
        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, facecolor=(0.9, 0.9, 0.9))
        plt.clf()
        plt.close("all")
        buf.seek(0)
        self.last_success_streak_img = Image.open(buf)


def play_string(text: str, language: str):
    try:
        speech = gTTS(text, lang=language, slow=False)
        mp3_fp = BytesIO()
        speech.write_to_fp(mp3_fp)
    except Exception as e:
        print(e)
        return
    mixer.init()
    mp3_fp.seek(0)
    mixer.music.load(mp3_fp, "mp3")
    mixer.music.play()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Util", epilog="Example: -")

    parser.add_argument("--text", "-t", required=True, type=str, help=f"Text to play.")
    parser.add_argument(
        "--language",
        "-l",
        required=False,
        type=str,
        default="de",
        help=f"Target language (default 'de')",
    )
    parser.add_argument(
        "--sleep", "-s", required=False, type=int, default=5, help=f"Sleep time"
    )
    args = parser.parse_args()

    play_string(text=args.text, language=args.language)

    time.sleep(int(args.sleep))
