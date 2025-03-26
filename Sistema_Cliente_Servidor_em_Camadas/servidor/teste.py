import requests

url = "http://localhost:5000/upload"
arquivo = {"file": open("imagem.jpg", "rb")}
dados = {"filtro": "invert"}

resposta = requests.post(url, files=arquivo, data=dados)

if resposta.status_code == 200:
    with open("imagem_modificada.png", "wb") as f:
        f.write(resposta.content)
else:
    print(resposta.json())  
