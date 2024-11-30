from flask import Flask, request, render_template
import requests
import json

app = Flask(__name__)

API_URL = "http://186.215.82.60:5009/process"  # URL da API externa
API_MK = "FPJ01072008"  # Chave para autenticação na API

def chamar_api_externa(prompt):
    """
    Faz a chamada à API externa para obter o conselho e versículos.
    """
    try:
        headers = {"Content-Type": "application/json"}
        payload = {"prompt": prompt, "mk": API_MK}
        
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            dados = response.json()  # Parse do JSON retornado pela API
            return dados.get("response", {})
        else:
            return {"conselho": "Erro ao obter conselho", "versiculos": []}
    except Exception as e:
        return {"conselho": "Erro ao conectar à API", "versiculos": []}

@app.route("/", methods=["GET", "POST"])
def index():
    conselho = ""
    versiculos = []
    
    if request.method == "POST":
        prompt_usuario = request.form["texto"]
        
        # Chamar a API externa com o prompt do usuário
        resultado = chamar_api_externa(prompt_usuario)
        
        # Processar os resultados
        if resultado:
            resposta = json.loads(resultado)  # Converter o texto JSON para um dicionário
            conselho = resposta.get("conselho", "Conselho não disponível")
            versiculos = resposta.get("versiculos", [])
    
    return render_template("index.html", conselho=conselho, versiculos=versiculos)

if __name__ == "__main__":
    app.run(debug=True)
