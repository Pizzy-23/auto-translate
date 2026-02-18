import tkinter as tk
import time
import queue

THEME_STYLES = {
    "dark": {"bg": "#2B2B2B", "fg": "#E0E0E0", "name": "Tema Dark"},
    "light": {"bg": "#EAEAEA", "fg": "#1C1C1C", "name": "Tema Light"},
    "gamer": {"bg": "#4B0082", "fg": "#00FF00", "name": "Tema Gamer"},
    "ocean": {"bg": "#005f73", "fg": "#ade8f4", "name": "Tema Oceano"},
    "purple_dark": {"bg": "#1e113b", "fg": "#d8b4fe", "name": "Tema Roxo Escuro"}
}

def tk_thread_worker(root, q):
    """Processa eventos da fila para garantir que o Tkinter só rode na thread principal."""
    while True:
        try:
            # Pega uma tarefa da fila sem bloquear para sempre
            action, args, response_event, result_container = q.get_nowait()
            
            # Se uma tarefa foi pega, processe-a
            try:
                if action == 'select_area':
                    selector = AreaSelector(root)
                    root.wait_window(selector)
                    result_container['result'] = selector.rect
                elif action == 'show_overlay':
                    text, x, y, style_key = args
                    OverlayWindow(root, style_key=style_key).show(text, x, y)
                
                if response_event:
                    response_event.set()
            finally:
                q.task_done()
        except queue.Empty:
            # Se a fila estiver vazia, atualiza a UI do Tkinter e dorme um pouco.
            try:
                root.update()
            except tk.TclError:
                break # A janela foi fechada, saia do loop
            time.sleep(0.05)

class AreaSelector(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.attributes('-fullscreen', True)
        self.attributes('-alpha', 0.3)
        self.attributes('-topmost', True)
        self.configure(bg='black')
        self.rect = None
        self.canvas = tk.Canvas(self, cursor="cross", highlightthickness=0, bg='black')
        self.canvas.pack(fill="both", expand=True)
        self.rect_item = None
        self.start_x = None
        self.start_y = None
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.bind("<Escape>", lambda e: self.destroy())
        
    def on_button_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.rect_item = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='cyan', width=2)
        
    def on_mouse_drag(self, event):
        self.canvas.coords(self.rect_item, self.start_x, self.start_y, event.x, event.y)
        
    def on_button_release(self, event):
        x1, y1 = self.start_x, self.start_y
        x2, y2 = event.x, event.y
        self.rect = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
        self.destroy()

class OverlayWindow(tk.Toplevel):
    def __init__(self, master, style_key='dark', duration_ms=5000):
        super().__init__(master)
        style = THEME_STYLES.get(style_key, THEME_STYLES['dark'])
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-disabled", True)
        # Tenta tornar o fundo da janela transparente (depende do OS)
        try:
            self.wm_attributes("-alpha", 0.9)
        except:
            pass
            
        self.configure(bg=style['bg'])
        self.label = tk.Label(
            self, 
            text="", 
            font=('Segoe UI', 16, 'bold'), 
            fg=style['fg'], 
            bg=style['bg'], 
            wraplength=600, 
            justify="center",
            padx=15,
            pady=10
        )
        self.label.pack()
        self.withdraw()
        self.after(duration_ms, self.destroy)
        
    def show(self, text, x, y):
        self.label.config(text=text)
        # Ajusta posição para não sair da tela (simplificado)
        self.geometry(f"+{int(x)}+{int(y-50)}") 
        self.deiconify()