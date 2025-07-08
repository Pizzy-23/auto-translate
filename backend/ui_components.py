import tkinter as tk

THEME_STYLES = {
    "dark": {"bg": "#2B2B2B", "fg": "#E0E0E0", "name": "Tema Dark"},
    "light": {"bg": "#EAEAEA", "fg": "#1C1C1C", "name": "Tema Light"},
    "gamer": {"bg": "#4B0082", "fg": "#00FF00", "name": "Tema Gamer"},
    "ocean": {"bg": "#005f73", "fg": "#ade8f4", "name": "Tema Oceano"},
    "purple_dark": {"bg": "#1e113b", "fg": "#d8b4fe", "name": "Tema Roxo Escuro"}
}

class AreaSelector(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.attributes('-fullscreen', True); self.attributes('-alpha', 0.3)
        self.configure(bg='black'); self.rect = None
        self.canvas = tk.Canvas(self, cursor="cross", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True); self.rect_item = None
        self.start_x = None; self.start_y = None
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.bind("<Escape>", lambda e: self.destroy())
    def on_button_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.rect_item = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)
    def on_mouse_drag(self, event):
        self.canvas.coords(self.rect_item, self.start_x, self.start_y, event.x, event.y)
    def on_button_release(self, event):
        x1, y1 = self.start_x, self.start_y; x2, y2 = event.x, event.y
        self.rect = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
        self.destroy()

class OverlayWindow(tk.Toplevel):
    def __init__(self, master, style_key='dark'):
        super().__init__(master)
        style = THEME_STYLES.get(style_key, THEME_STYLES['dark'])
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True); self.wm_attributes("-disabled", True)
        self.wm_attributes("-transparentcolor", "white"); self.configure(bg='white')
        self.label = tk.Label(self, text="", font=('Arial', '18', 'bold'), 
                              fg=style['fg'], bg=style['bg'], wraplength=800, justify="left")
        self.label.pack(padx=10, pady=5); self.withdraw()
    def show(self, text, x, y):
        self.label.config(text=text)
        self.geometry(f"+{int(x-10)}+{int(y-10)}"); self.deiconify()