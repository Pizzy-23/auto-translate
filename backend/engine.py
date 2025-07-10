import mss
from PIL import Image
import time
import threading
import json
from ocr_engine import run_ocr
from translator import translate_text

class TranslationEngine:
    def __init__(self):
        self.is_realtime_running = False
        self.thread = None; self.area = None; self.last_text = ""
        self.update_callback = None

    def register_update_callback(self, callback): self.update_callback = callback
    def unregister_update_callback(self): self.update_callback = None

    def translate_single_area(self, settings, tk_queue):
        area_dict = self._select_area_via_queue(tk_queue)
        if not area_dict: return {"error": "Seleção cancelada."}
        return self._process_frame(settings, area_dict, tk_queue)

    def start_realtime_loop(self, settings, tk_queue):
        if self.is_realtime_running: return {"error": "Modo tempo real já ativo."}
        area_dict = self._select_area_via_queue(tk_queue)
        if not area_dict: return {"error": "Seleção cancelada."}
        self.area = area_dict; self.is_realtime_running = True
        self.last_text = ""
        self.thread = threading.Thread(target=self._translation_loop, args=(settings, tk_queue), daemon=True)
        self.thread.start()
        return {"status": "success", "logs": ["Modo tempo real iniciado."]}

    def stop_realtime_loop(self):
        self.is_realtime_running = False
        if self.thread and self.thread.is_alive(): self.thread.join(timeout=1.5)
        print("[Engine] Loop parado.")
        return {"status": "success", "logs": ["Tradução parada."]}
        
    def _translation_loop(self, settings, tk_queue):
        while self.is_realtime_running:
            result = self._process_frame(settings, self.area, tk_queue, from_loop=True)
            if result and self.update_callback:
                try: self.update_callback(json.dumps(result))
                except Exception as e: print(f"[WebSocket] Erro ao enviar dados: {e}")
            time.sleep(2.0)

    def _process_frame(self, settings, area, tk_queue=None, from_loop=False):
        with mss.mss() as sct:
            sct_img = sct.grab(area)
            pil_image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        
        original_text = run_ocr(pil_image, lang=settings['src_codes'][0])
        if not original_text or (from_loop and original_text == self.last_text): return None
        
        self.last_text = original_text
        translation = translate_text(original_text, src_lang=settings['src_codes'][1], dest_lang=settings['dest_codes'][1])
        if not translation: return None
        
        if settings['output_mode'] == 'overlay' and tk_queue:
            self.show_overlay_via_queue(translation, area, settings['style_key'], tk_queue)
        
        return {"original_text": original_text, "translated_text": translation}

    def _select_area_via_queue(self, tk_queue):
        response_event = threading.Event()
        result_container = {}; tk_queue.put(('select_area', (), response_event, result_container))
        response_event.wait(timeout=60)
        rect = result_container.get('result')
        if not rect: return None
        x1, y1, x2, y2 = rect
        return {'left': int(x1), 'top': int(y1), 'width': int(x2 - x1), 'height': int(y2 - y1)}

    def show_overlay_via_queue(self, text, area, style_key, tk_queue):
        args = (text, area['left'], area['top'], style_key)
        tk_queue.put(('show_overlay', args, None, {}))

engine_instance = TranslationEngine()