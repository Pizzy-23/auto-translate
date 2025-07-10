import queue
import threading
import tkinter as tk
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sock import Sock
from engine import engine_instance
from ui_components import THEME_STYLES, tk_thread_worker

# Configuração da aplicação
tk_queue = queue.Queue()
LANG_MAP = {"Inglês": ['eng', 'en'],"Português": ['por', 'pt'],"Japonês": ['jpn', 'ja']}
app = Flask(__name__)
CORS(app)
sock = Sock(app)

# === WebSocket Endpoint ===
@sock.route('/ws-updates')
def ws_updates(ws):
    print("[WebSocket] Cliente conectado.")
    engine_instance.register_update_callback(ws.send)
    try:
        while True: ws.receive(timeout=10) # Mantém a conexão aberta
    except Exception:
        print("[WebSocket] Cliente desconectado.")
    finally:
        engine_instance.unregister_update_callback()

# === HTTP API Endpoints ===
def get_settings(data):
    return {
        "output_mode": data.get('output_mode', 'app'),
        "style_key": data.get('style_key', 'dark'),
        "source_lang": data.get('source_lang', 'Inglês'),
        "target_lang": data.get('target_lang', 'Português'),
        "src_codes": LANG_MAP.get(data.get('source_lang', 'Inglês')),
        "dest_codes": LANG_MAP.get(data.get('target_lang', 'Português')),
    }

@app.route('/get-themes', methods=['GET'])
def get_themes(): return jsonify(THEME_STYLES)

@app.route('/translate-once', methods=['POST'])
def translate_once():
    settings = get_settings(request.json)
    settings['translation_mode'] = 'single'
    result = engine_instance.translate_single_area(settings, tk_queue)
    return jsonify(result)

@app.route('/start-realtime', methods=['POST'])
def start_realtime():
    settings = get_settings(request.json)
    settings['translation_mode'] = 'realtime'
    result = engine_instance.start_realtime_loop(settings, tk_queue)
    return jsonify(result)

@app.route('/stop-realtime', methods=['POST'])
def stop_realtime():
    return jsonify(engine_instance.stop_realtime_loop())

if __name__ == '__main__':
    # 1. Inicia o Flask em uma thread separada para não bloquear a thread principal
    flask_thread = threading.Thread(
        target=lambda: app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False),
        daemon=True
    )
    flask_thread.start()
    print("Servidor Flask e WebSocket iniciado em http://127.0.0.1:5000")
    
    # 2. Roda a fila Tkinter na thread principal, onde ela é segura.
    root = tk.Tk()
    root.withdraw()
    tk_thread_worker(root, tk_queue) # Essa função entra em um loop infinito