from flask import Flask, request, jsonify, send_file
import os
import sqlite3
from datetime import datetime
from PIL import Image, ImageFilter

app = Flask(__name__)
DATABASE = 'metadados.db'

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

PROCESSED_FOLDER = 'processed'
if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS metadados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                filtro TEXT,
                data_hora TEXT
            )
        ''')
        conn.commit()

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'erro': 'Nenhuma imagem enviada'}), 400

    arquivo = request.files['image']
    if arquivo.filename == '':
        return jsonify({'erro': 'Nome do arquivo vazio'}), 400

    caminho_original = os.path.join(UPLOAD_FOLDER, arquivo.filename)
    arquivo.save(caminho_original)

    caminho_modificado = aplicar_filtro(caminho_original)

    if not caminho_modificado:
        return jsonify({"erro": "Erro ao processar a imagem"}), 500

    return send_file(caminho_modificado, mimetype="image/png")

def aplicar_filtro(caminho_imagem):
    try:
        imagem = Image.open(caminho_imagem)
        imagem = imagem.convert("L")  # Exemplo de filtro: converter para grayscale
        caminho_modificado = os.path.join(PROCESSED_FOLDER, 'mod_imagem.jpg')
        imagem.save(caminho_modificado)
        return caminho_modificado
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        return None

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port="5000", debug=True) 