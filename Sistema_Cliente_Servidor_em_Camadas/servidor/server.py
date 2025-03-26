from flask import Flask, request, jsonify, send_file
import os
from datetime import datetime
from PIL import Image, ImageOps
import random  # Adicione esta importação no início do arquivo

app = Flask(__name__)

UPLOAD_FOLDER = os.path.abspath('uploads')
PROCESSED_FOLDER = os.path.abspath('processed')

def aplicar_filtro(imagem_path, filtro):
    try:
        img = Image.open(imagem_path)

        if filtro == "invert":
            img = ImageOps.invert(img.convert("RGB"))
        elif filtro == "grayscale":
            img = ImageOps.grayscale(img)
        elif filtro == "mirror":
            img = ImageOps.mirror(img)
        else:
            print("Filtro não reconhecido.")
            return None  

        nome_arquivo = os.path.basename(imagem_path)
        # Mantém o nome original e adiciona um sufixo "_modificado"
        caminho_modificado = os.path.join(PROCESSED_FOLDER, f'mod_{nome_arquivo}')
        
        # Verifica se a pasta existe
        if not os.path.exists(PROCESSED_FOLDER):
            os.makedirs(PROCESSED_FOLDER)

        img.save(caminho_modificado)
        print(f"Imagem processada salva em: {caminho_modificado}")

        return caminho_modificado
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        return None

@app.route("/upload", methods=["POST"])
def upload():
    print("Recebendo a requisição...")
    if "image" not in request.files:
        print("Nenhuma imagem enviada.")
        return jsonify({"erro": "Nenhuma imagem enviada"}), 400

    print(request.files)

    arquivo = request.files["image"]
    print(f"Arquivo recebido: {arquivo.filename}")

    filtro = request.form.get("filtro", "grayscale")  

    if arquivo.filename == "":
        print("Nome do arquivo vazio.")
        return jsonify({"erro": "Nome do arquivo vazio"}), 400

    # Cria o diretório se não existir
    if not os.path.exists(PROCESSED_FOLDER):
        os.makedirs(PROCESSED_FOLDER)

    # Salva a imagem original
    caminho_original = os.path.join(UPLOAD_FOLDER, arquivo.filename)
    print(f"Salvando imagem original em: {caminho_original}")
    arquivo.save(caminho_original)

    # Aplica o filtro e salva a imagem processada
    caminho_modificado = aplicar_filtro(caminho_original, filtro)

    if not caminho_modificado:
        print("Erro ao processar a imagem.")
        return jsonify({"erro": "Erro ao processar a imagem"}), 500

    print(f"Imagem processada salva em: {caminho_modificado}")

    # Retorna as URLs das imagens
    return jsonify({
        'original_url': caminho_original,
        'modified_url': caminho_modificado
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
