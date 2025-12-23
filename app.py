from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MODELOS (carregam uma vez)
resumidor = pipeline("summarization", model="csebuetnlp/mT5_multilingual_XLSum")
tradutor_pt_en = pipeline("translation_pt_to_en", model="Helsinki-NLP/opus-mt-pt-en")
tradutor_en_pt = pipeline("translation_en_to_pt", model="Helsinki-NLP/opus-mt-en-pt")
sentimento = pipeline("sentiment-analysis")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/resumir", methods=["POST"])
def resumir():
    texto = request.json["texto"]
    resumo = resumidor(texto, max_length=80, min_length=20, do_sample=False)
    return jsonify({"resultado": resumo[0]["summary_text"]})

@app.route("/traduzir_pt_en", methods=["POST"])
def traduzir_pt_en():
    texto = request.json["texto"]
    traducao = tradutor_pt_en(texto)
    return jsonify({"resultado": traducao[0]["translation_text"]})

@app.route("/traduzir_en_pt", methods=["POST"])
def traduzir_en_pt():
    texto = request.json["texto"]
    traducao = tradutor_en_pt(texto)
    return jsonify({"resultado": traducao[0]["translation_text"]})

@app.route("/sentimento", methods=["POST"])
def analisar_sentimento():
    texto = request.json["texto"]
    result = sentimento(texto)
    return jsonify({
        "resultado": f"{result[0]['label']} ({round(result[0]['score'], 2)})"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
