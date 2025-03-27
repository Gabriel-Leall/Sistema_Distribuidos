from flask import Flask, request, jsonify, send_file, send_from_directory
import os
import sqlite3
from datetime import datetime
from PIL import Image, ImageFilter

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)

DATABASE = os.path.join(BASE_DIR, "database", "metadados.db")

if not os.path.exists(DATABASE):
    raise FileNotFoundError(f"Erro: O banco de dados não foi encontrado em {DATABASE}")

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
PROCESSED_FOLDER = os.path.join(BASE_DIR, 'processed')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

app.add_url_rule('/uploads/<filename>', endpoint='uploaded_file', view_func=lambda filename: send_from_directory(UPLOAD_FOLDER, filename))
app.add_url_rule('/processed/<filename>', endpoint='processed_file', view_func=lambda filename: send_from_directory(PROCESSED_FOLDER, filename))

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
    filtro = request.form.get("filtro", "grayscale")  

    if arquivo.filename == "":
        print("Nome do arquivo vazio.")
        return jsonify({"erro": "Nome do arquivo vazio"}), 400

    caminho_original = os.path.join(UPLOAD_FOLDER, arquivo.filename)
    arquivo.save(caminho_original)

    caminho_modificado = aplicar_filtro(caminho_original, filtro)

    if not caminho_modificado:
        print("Erro ao processar a imagem.")
        return jsonify({"erro": "Erro ao processar a imagem"}), 500

    salvar_metadados(arquivo.filename, filtro)

    return jsonify({
        'original_url': f"/uploads/{arquivo.filename}",
        'modified_url': f"/processed/{os.path.basename(caminho_modificado)}"
    })

def aplicar_filtro(caminho_imagem, filtro):
    try:
        imagem = Image.open(caminho_imagem)

        if filtro == "invert":
            imagem = imagem.convert("RGB").transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
        elif filtro == "grayscale":
            imagem = imagem.convert("L")
        elif filtro == "mirror":
            imagem = imagem.transpose(Image.FLIP_LEFT_RIGHT)
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

def salvar_metadados(nome_arquivo, filtro):
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO metadados (nome, filtro, data_hora)
                VALUES (?, ?, ?)
            ''', (nome_arquivo, filtro, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
        print(f"Metadados salvos: {nome_arquivo}, {filtro}")
    except Exception as e:
        print(f"Erro ao salvar metadados: {e}")

if __name__ == '__main__':
    init_db()
    print("🚀 Servidor rodando em http://0.0.0.0:5000 🚀")
    app.run(host="0.0.0.0", port=5000, debug=True)
