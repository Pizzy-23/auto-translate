from flask import Flask, jsonify, request
from flask_cors import CORS
import engine
from ui_components import THEME_STYLES

LANG_MAP = {"Inglês": ['eng', 'en'],"Português": ['por', 'pt'],"Japonês": ['jpn', 'ja']}
app = Flask(__name__)
CORS(app)



@app.route('/get-themes', methods=['GET'])
def get_themes():
    return jsonify(THEME_STYLES)

def get_settings(data):
    return {
        "output_mode": data.get('output_mode', 'app'),
        "style_key": data.get('style_key', 'dark'),
        "src_codes": LANG_MAP.get(data.get('source_lang', 'Inglês')),
        "dest_codes": LANG_MAP.get(data.get('target_lang', 'Português')),
    }

@app.route('/translate-once', methods=['POST'])
def translate_once():
    settings = get_settings(request.json)
    return jsonify(engine.engine_instance.translate_single_area(settings))

@app.route('/start-realtime', methods=['POST'])
def start_realtime():
    settings = get_settings(request.json)
    return jsonify(engine.engine_instance.start_realtime_loop(settings))

@app.route('/stop-realtime', methods=['POST'])
def stop_realtime():
    return jsonify(engine.engine_instance.stop_realtime_loop())


if __name__ == '__main__':
    print("Iniciando servidor Flask em MODO DE DESENVOLVIMENTO (com auto-reload)...")
    app.run(port=5000, debug=True, threaded=False)