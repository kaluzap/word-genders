import tkinter as tk
from util.control_frame import ControlFrame


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.wm_title("WORDS!")
        self.geometry("550x500")
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.resizable(False, False)
        self._frame = None
        self.ControlFrame = ControlFrame
        self.switch_frame(ControlFrame)
    
    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        
    def close_window(self):
        print("Ciao")
        quit()

        
def main():
    app = App()
    #ControlFrame(app)
    app.mainloop()
    

if __name__ == "__main__":
    main()
