import subprocess
from PIL import ImageEnhance, Image
import tempfile
import os

TESSERACT_PATH = r'C:\Tesseract-OCR\tesseract.exe'

def run_ocr(pil_image, lang='eng'):
    """
    Realiza pré-processamento, salva a imagem em um arquivo temporário (mais
    robusto para Windows) e executa o Tesseract.
    """
    text_data = ""
    temp_img_path = None
    
    try:
        img = pil_image.convert('L')
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
        img = img.point(lambda p: 255 if p > 135 else 0)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_img:
            temp_img_path = temp_img.name
            img.save(temp_img_path)

        command = [TESSERACT_PATH, temp_img_path, 'stdout', '-l', lang, '--psm', '6']
        
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding='utf-8',
            check=False
        )

        if process.returncode == 0:
            text_data = process.stdout.strip()
            print("[OCR Engine] Texto detectado com sucesso!")
        else:
            error_details = process.stderr.strip()
            print(f"[OCR Engine] Tesseract falhou. Erro: {error_details}")
            text_data = "" 

    except FileNotFoundError:
        print(f"[OCR Engine] ERRO CRÍTICO: Tesseract não encontrado em '{TESSERACT_PATH}'.")
        text_data = f"ERRO: Tesseract não encontrado."
    except Exception as e:
        print(f"[OCR Engine] Erro inesperado durante o OCR: {e}")
        text_data = f"ERRO: {e}"
    finally:
        if temp_img_path and os.path.exists(temp_img_path):
            os.remove(temp_img_path)
            
    return text_data