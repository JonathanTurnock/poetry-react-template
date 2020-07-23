from os import path
from pathlib import Path

from flask import Flask, send_from_directory, jsonify

from server.health import get_app_health

app = Flask(__name__)


@app.route('/')
def index():
    return send_from_directory(web_root, 'index.html')


@app.route('/<file>')
def web(file):
    if path.exists(Path(web_root, file)):
        return send_from_directory(web_root, file)
    else:
        return index()


@app.route('/api/health', methods=['GET'])
def check_health():
    return jsonify(get_app_health())
