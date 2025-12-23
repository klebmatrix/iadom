from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/ping")
def ping():
    return {"status": "ok"}

@app.route("/resumir", methods=["POST"])
def resumir():
    texto = request.json.get("texto", "")
    return jsonify({"resultado": texto[:50]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
