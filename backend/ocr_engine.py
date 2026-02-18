import subprocess
from PIL import ImageEnhance, Image
import tempfile
import os

TESSERACT_PATH = r'C:\Tesseract-OCR\tesseract.exe'

def run_ocr(pil_image, lang='eng'):
    """
    Realiza pré-processamento, salva a imagem em um arquivo temporário (mais
    robusto para Windows) e executa o Tesseract com parâmetros otimizados.
    """
    text_data = ""
    temp_img_path = None
    
    try:
        # Melhorando o pré-processamento para OCR
        img = pil_image.convert('L')
        
        # Aumentar tamanho ajuda o Tesseract com fontes pequenas
        w, h = img.size
        img = img.resize((w*2, h*2), Image.Resampling.LANCZOS)
        
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.5)
        img = img.point(lambda p: 255 if p > 140 else 0)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_img:
            temp_img_path = temp_img.name
            img.save(temp_img_path)

        # PSM 6: Assume um único bloco de texto uniforme
        # --oem 3: Usa o motor LSTM padrão
        command = [TESSERACT_PATH, temp_img_path, 'stdout', '-l', lang, '--psm', '6', '--oem', '3']
        
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding='utf-8',
            check=False,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )

        if process.returncode == 0:
            text_data = process.stdout.strip()
            # Limpeza básica de caracteres que costumam vir errados no OCR
            text_data = text_data.replace('|', 'I').replace('`', "'").replace('  ', ' ')
            if text_data:
                print(f"[OCR Engine] Texto detectado: {text_data[:40]}...")
        else:
            error_details = process.stderr.strip()
            print(f"[OCR Engine] Tesseract falhou. Erro: {error_details}")
            text_data = "" 

    except FileNotFoundError:
        print(f"[OCR Engine] ERRO CRÍTICO: Tesseract não encontrado em '{TESSERACT_PATH}'.")
        text_data = "ERRO: Tesseract não encontrado."
    except Exception as e:
        print(f"[OCR Engine] Erro inesperado durante o OCR: {e}")
        text_data = f"ERRO: {e}"
    finally:
        if temp_img_path and os.path.exists(temp_img_path):
            try: os.remove(temp_img_path)
            except: pass
            
    return text_data