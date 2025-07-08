from flask import Flask, jsonify, request
from flask_cors import CORS
import engine
from ui_components import THEME_STYLES

LANG_MAP = {
    "Inglês": ['eng', 'en'], "Português": ['por', 'pt'],
    "Japonês": ['jpn', 'ja'], "Espanhol": ['spa', 'es']
}
app = Flask(__name__)
CORS(app)

@app.route('/get-themes', methods=['GET'])
def get_themes():
    return jsonify(THEME_STYLES)

@app.route('/translate-area', methods=['POST'])
def translate_area():
    data = request.json
    source_lang = data.get('source_lang', 'Inglês')
    target_lang = data.get('target_lang', 'Português')
    output_mode = data.get('output_mode', 'app')
    style_key = data.get('style_key', 'dark')

    src_codes = LANG_MAP.get(source_lang, LANG_MAP['Inglês'])
    dest_codes = LANG_MAP.get(target_lang, LANG_MAP['Português'])

    result = engine.select_and_translate(src_codes, dest_codes, output_mode, style_key)
    
    return jsonify(result)

if __name__ == '__main__':
    print("Iniciando servidor Flask em http://127.0.0.1:5000")
    app.run(port=5000, debug=False, threaded=False)