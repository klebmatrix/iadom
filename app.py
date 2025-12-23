from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 🔴 NECESSÁRIO para o index.html funcionar

@app.route("/")
def home():
    return "API IA DOM ONLINE"

@app.route("/resumir", methods=["POST"])
def resumir():
    data = request.get_json(silent=True)

    if not data or "texto" not in data:
        return jsonify({"resultado": "Texto não enviado"}), 400

    texto = data["texto"]

    # resumo SIMPLES (funciona sempre)
    resumo = texto[:120] + "..." if len(texto) > 120 else texto

    return jsonify({"resultado": resumo})

@app.route("/traduzir_pt_en", methods=["POST"])
def traduzir_pt_en():
    data = request.get_json(silent=True)
    return jsonify({"resultado": "Tradução PT→EN (mock funcionando)"})

@app.route("/traduzir_en_pt", methods=["POST"])
def traduzir_en_pt():
    data = request.get_json(silent=True)
    return jsonify({"resultado": "Tradução EN→PT (mock funcionando)"})

@app.route("/sentimento", methods=["POST"])
def sentimento():
    data = request.get_json(silent=True)
    return jsonify({"resultado": "Sentimento: NEUTRO (mock)"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
