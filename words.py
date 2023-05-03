import tkinter as tk
from frames.control_frame import ControlFrame
from frames.nouns_frame import NounsFrame
from frames.add_delete_frame import AddDeleteFrame

# from frames.meanings_frame import MeaningsFrame
from util.dictionary import Dictionary
from configuration.configuration import Configuration

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        #self.protocol("WM_DELETE_WINDOW", self.close_window)
        
        self.dictionary = Dictionary()
        self.configuration = Configuration()

        self.all_frames = {"control": ControlFrame, "nouns": NounsFrame, "add_delete":AddDeleteFrame}
        self._frame = None
        self.switch_frame("control")

    def switch_frame(self, frame_name: str):
        """Destroys current frame and replaces it with a new one."""
        new_frame = self.all_frames[frame_name](self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def close_window(self):
        print("Ciao")
        quit()


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
