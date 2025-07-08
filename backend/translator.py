from googletrans import Translator

def translate_text(text, src_lang, dest_lang):
    """
    Usa o googletrans para traduzir o texto.
    """
    if not text:
        return ""
        
    try:
        translator = Translator()
        translation = translator.translate(text, src=src_lang, dest=dest_lang)
        return translation.text
    except Exception as e:
        print(f"[Translator] Erro no Google Translate: {e}")
        return None