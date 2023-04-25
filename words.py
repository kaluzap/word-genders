import tkinter as tk
from util.control_frame import ControlFrame


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.wm_title("WORDS!")
        self.geometry("550x500")
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.resizable(False, False)

    def close_window(self):
        print("Ciao")
        quit()

        
def main():
    app = App()
    ControlFrame(app)
    app.mainloop()
    

if __name__ == "__main__":
    main()
