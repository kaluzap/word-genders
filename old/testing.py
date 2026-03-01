import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dynamic Resize App")

        # Mapping frames to their specific (Width x Height) and Background Color
        self.frame_config = {
            "control": {"class": ControlFrame, "size": "700x500", "color": "white"},
            "nouns": {"class": NounsFrame, "size": "100x100", "color": "lightblue"},
            "manage_words": {"class": ManageWordsFrame, "size": "200x200", "color": "lightgreen"},
            "meanings": {"class": MeaningsFrame, "size": "300x300", "color": "lightyellow"},
        }

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self.init_frames()
        self.switch_frame("control")

    def init_frames(self):
        """Pre-loads all frames into the dictionary."""
        for name, config in self.frame_config.items():
            # Pass controller and background color to each frame
            frame = config["class"](parent=self.container, controller=self, bg=config["color"])
            self.frames[name] = frame
            frame.grid(row=0, column=0)#, sticky="nsew")

    def switch_frame(self, frame_name: str):
        """Updates window size and brings frame to front."""
        if frame_name in self.frame_config:
            # 1. Update the main window size
            new_size = self.frame_config[frame_name]["size"]
            new_frame = self.frame_config[frame_name]["class"]

            if new_frame:
                self.geometry(new_size)

            # 2. Raise the requested frame
                new_frame.tkraise()


    # def switch_frame(self, frame_name: str):
    #     """Raises the requested frame to the top."""
    #     frame = self.frames.get(frame_name)
    #     if frame:
    #         frame.tkraise()
    #     else:
    #         print(f"Error: Frame '{frame_name}' not found.")

class BaseFrame(tk.Frame):
    """Parent frame to handle common layout."""
    def __init__(self, parent, controller, bg):
        super().__init__(parent, bg=bg)
        # Optional: Prevent widgets from shrinking the frame
        self.pack_propagate(0)

class ControlFrame(BaseFrame):
    def __init__(self, parent, controller, bg):
        super().__init__(parent, controller, bg)
        tk.Label(self, text="Main (400x500)", bg=bg).pack(pady=10)
        tk.Button(self, text="To 100x100", command=lambda: controller.switch_frame("nouns")).pack()
        tk.Button(self, text="To 200x200", command=lambda: controller.switch_frame("manage_words")).pack()
        tk.Button(self, text="To 300x300", command=lambda: controller.switch_frame("meanings")).pack()

class NounsFrame(BaseFrame):
    def __init__(self, parent, controller, bg):
        super().__init__(parent, controller, bg)
        tk.Button(self, text="Back", command=lambda: controller.switch_frame("control")).pack(expand=True)

class ManageWordsFrame(BaseFrame):
    def __init__(self, parent, controller, bg):
        super().__init__(parent, controller, bg)
        tk.Button(self, text="Back", command=lambda: controller.switch_frame("control")).pack(expand=True)

class MeaningsFrame(BaseFrame):
    def __init__(self, parent, controller, bg):
        super().__init__(parent, controller, bg)
        tk.Button(self, text="Back", command=lambda: controller.switch_frame("control")).pack(expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
