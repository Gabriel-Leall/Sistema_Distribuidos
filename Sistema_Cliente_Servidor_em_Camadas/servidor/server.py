from flask import Flask, request, jsonify, send_file
import os
from datetime import datetime
from PIL import Image, ImageOps

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

def aplicar_filtro(imagem_path, filtro):
    img = Image.open(imagem_path)

    if filtro == "invert":
        img = ImageOps.invert(img.convert("RGB"))
    elif filtro == "grayscale":
        img = ImageOps.grayscale(img)
    elif filtro == "mirror":
        img = ImageOps.mirror(img)
    else:
        return None  

    nome_arquivo = os.path.basename(imagem_path)
    caminho_modificado = os.path.join(PROCESSED_FOLDER, f"mod_{nome_arquivo}")
    img.save(caminho_modificado)

    return caminho_modificado

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"erro": "Nenhuma imagem enviada"}), 400

    arquivo = request.files["file"]
    filtro = request.form.get("filtro", "grayscale")  

    if arquivo.filename == "":
        return jsonify({"erro": "Nome do arquivo vazio"}), 400

    caminho_original = os.path.join(UPLOAD_FOLDER, arquivo.filename)
    arquivo.save(caminho_original)

    caminho_modificado = aplicar_filtro(caminho_original, filtro)

    if not caminho_modificado:
        return jsonify({"erro": "Filtro inválido"}), 400

    return send_file(caminho_modificado, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
