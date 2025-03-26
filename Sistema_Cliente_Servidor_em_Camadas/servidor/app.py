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

@app.route("/upload", methods=["POST"])
def upload():
    print("Recebendo a requisição...")
    if "image" not in request.files:
        print("Nenhuma imagem enviada.")
        return jsonify({"erro": "Nenhuma imagem enviada"}), 400

    arquivo = request.files["image"]
    filtro = request.form.get("filtro", "grayscale")  # Pega o filtro enviado

    if arquivo.filename == "":
        print("Nome do arquivo vazio.")
        return jsonify({"erro": "Nome do arquivo vazio"}), 400

    # Salva a imagem original
    caminho_original = os.path.join(UPLOAD_FOLDER, arquivo.filename)
    arquivo.save(caminho_original)

    # Aplica o filtro e salva a imagem processada
    caminho_modificado = aplicar_filtro(caminho_original, filtro)

    if not caminho_modificado:
        print("Erro ao processar a imagem.")
        return jsonify({"erro": "Erro ao processar a imagem"}), 500

    return jsonify({
        'original_url': caminho_original,
        'modified_url': caminho_modificado
    })

def aplicar_filtro(caminho_imagem, filtro):
    try:
        imagem = Image.open(caminho_imagem)

        if filtro == "invert":
            imagem = Image.open(caminho_imagem).convert("RGB").transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
        elif filtro == "grayscale":
            imagem = Image.open(caminho_imagem).convert("L")
        elif filtro == "mirror":
            imagem = Image.open(caminho_imagem).transpose(Image.FLIP_LEFT_RIGHT)
        else:
            print("Filtro não reconhecido.")
            return None

        nome_arquivo = os.path.basename(caminho_imagem)
        caminho_modificado = os.path.join(PROCESSED_FOLDER, f'mod_{nome_arquivo}')
        imagem.save(caminho_modificado)
        return caminho_modificado
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        return None

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port="5000", debug=True) 