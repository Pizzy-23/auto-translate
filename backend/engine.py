import tkinter as tk
import mss
from PIL import Image
import time
import threading
from ui_components import AreaSelector, OverlayWindow
from ocr_engine import run_ocr
from translator import translate_text

class TranslationEngine:
    def __init__(self):
        self.is_realtime_running = False
        self.thread = None
        self.area = None
        self.last_text = ""

    def translate_single_area(self, settings):
        area_dict = self._select_area()
        if not area_dict: return {"error": "Seleção cancelada."}
        return self._process_frame_and_translate(settings, area_dict)

    def start_realtime_loop(self, settings):
        if self.is_realtime_running: return {"error": "Modo tempo real já ativo."}
        area_dict = self._select_area()
        if not area_dict: return {"error": "Seleção cancelada."}
        self.area = area_dict
        self.is_realtime_running = True
        self.thread = threading.Thread(target=self._translation_loop, args=(settings,), daemon=True)
        self.thread.start()
        return {"status": "success", "logs": ["Modo tempo real iniciado."]}

    def stop_realtime_loop(self):
        self.is_realtime_running = False
        if self.thread and self.thread.is_alive(): self.thread.join(timeout=1.5)
        print("[Engine] Loop parado.")
        return {"status": "success", "logs": ["Tradução parada."]}
        
    def _translation_loop(self, settings):
        with mss.mss() as sct:
            while self.is_realtime_running:
                self._process_frame_and_translate(settings, self.area, sct_instance=sct)
                time.sleep(2.0)

    def _process_frame_and_translate(self, settings, area, sct_instance=None):
        sct = sct_instance or mss.mss()
        with sct:
            pil_image = Image.frombytes("RGB", sct.grab(area).size, sct.grab(area).bgra, "raw", "BGRX")
        
        original_text = run_ocr(pil_image, lang=settings['src_codes'][0])
        if not original_text or (original_text == self.last_text and settings.get('translation_mode') == 'realtime'): return None
        
        self.last_text = original_text
        translation = translate_text(original_text, src_lang=settings['src_codes'][1], dest_lang=settings['dest_codes'][1])
        if not translation: return None

        if settings['output_mode'] == 'overlay':
            overlay_thread = threading.Thread(target=self._show_overlay_in_thread, args=(translation, area['left'], area['top'], settings['style_key']), daemon=True)
            overlay_thread.start()
        
        return {"original_text": original_text, "translated_text": translation, "logs": ["Tradução processada."]}
        
    def _show_overlay_in_thread(self, text, x, y, style_key):
        root = tk.Tk(); root.withdraw()
        overlay = OverlayWindow(root, style_key=style_key); overlay.show(text, x, y); root.mainloop()

    def _select_area(self):
        root = tk.Tk(); root.withdraw()
        selector = AreaSelector(root); root.wait_window(selector); root.destroy()
        if not selector.rect: return None
        x1, y1, x2, y2 = selector.rect
        return {'left': x1, 'top': y1, 'width': x2 - x1, 'height': y2 - y1}

engine_instance = TranslationEngine()