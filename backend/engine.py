import tkinter as tk
import mss
from PIL import Image
from ui_components import AreaSelector, OverlayWindow
from ocr_engine import run_ocr
from translator import translate_text

def select_and_translate(src_codes, dest_codes, output_mode, style_key):
    root = tk.Tk()
    root.withdraw()
    selector = AreaSelector(root)
    root.wait_window(selector)
    if not selector.rect:
        root.destroy()
        return {"error": "Seleção de área cancelada."}

    x1, y1, x2, y2 = selector.rect
    area = {'left': x1, 'top': y1, 'width': x2 - x1, 'height': y2 - y1}
    with mss.mss() as sct:
        sct_img = sct.grab(area)
        pil_image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
    original_text = run_ocr(pil_image, lang=src_codes[0])
    if not original_text:
        root.destroy()
        return {"original_text": "", "translated_text": "", "logs": ["Nenhum texto detectado."]}
    translation = translate_text(original_text, src_lang=src_codes[1], dest_lang=dest_codes[1])
    if translation is None:
        root.destroy()
        return {"error": "Falha na tradução."}

    if output_mode == 'overlay':
        overlay = OverlayWindow(root, style_key=style_key)
        overlay.show(translation, x1, y1)
        root.after(5000, root.destroy)
    else:
        root.destroy()
    return {
        "original_text": original_text,
        "translated_text": translation,
        "logs": ["Processo concluído com sucesso."]
    }