from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Token do Hugging Face
HUGGING_FACE_TOKEN = "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"

# Função para gerar conselho
def gerar_conselho(texto_usuario):
    url = "https://api-inference.huggingface.co/models/bigscience/bloomz-560m"
    headers = {"Authorization": f"Bearer {HUGGING_FACE_TOKEN}"}
    payload = {"inputs": f"Conselho para a situação: {texto_usuario}"}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    return "Não foi possível gerar o conselho no momento."

# Função para buscar versículo bíblico
def buscar_versiculo():
    url = "https://www.abibliadigital.com.br/api/verses/nvi/random"
    response = requests.get(url)
    if response.status_code == 200:
        versiculo = response.json()
        return f"{versiculo['text']} - {versiculo['book']['name']} {versiculo['chapter']}:{versiculo['number']}"
    return "Não foi possível buscar um versículo no momento."

@app.route("/", methods=["GET", "POST"])
def index():
    conselho = ""
    versiculo = ""
    if request.method == "POST":
        texto_usuario = request.form["texto"]
        conselho = gerar_conselho(texto_usuario)
        versiculo = buscar_versiculo()
    return render_template("index.html", conselho=conselho, versiculo=versiculo)

if __name__ == "__main__":
    import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

