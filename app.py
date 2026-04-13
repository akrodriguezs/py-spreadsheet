import customtkinter as ctk
from views.grid_view import GridView

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("900x600")
        self.title("Mini Excel 🔥")

        # 🔥 layout responsive real
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.grid_view = GridView(self)
        self.bind("<Configure>", self.on_resize)
        self.grid_view.grid(row=0, column=0, sticky="nsew")
    def on_resize(self, event):
        # evita recalculos excesivos
        if hasattr(self, "_resizing"):
            return

        self._resizing = True
        self.after(16, self.finish_resize)  # ~60fps   
    def finish_resize(self):
        self._resizing = False    