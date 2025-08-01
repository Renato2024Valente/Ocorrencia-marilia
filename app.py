from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# Conexão com MongoDB Atlas
client = MongoClient("mongodb+srv://bicudo:bicudo25@cluster0.1txkr5t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["ocorrencias"]
colecao = db["registros"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/listar")
def listar():
    return render_template("listar.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/ocorrencias", methods=["POST"])
def registrar_ocorrencia():
    dados = request.json
    dados["dataHora"] = datetime.now()
    colecao.insert_one(dados)
    return jsonify({"mensagem": "Ocorrência registrada com sucesso."}), 201

@app.route("/ocorrencias", methods=["GET"])
def listar_ocorrencias():
    registros = list(colecao.find().sort("dataHora", -1))
    for r in registros:
        r["_id"] = str(r["_id"])
        r["dataHora"] = r["dataHora"].isoformat()
    return jsonify(registros)

@app.route("/ocorrencias/<id>", methods=["DELETE"])
def deletar_ocorrencia(id):
    colecao.delete_one({"_id": ObjectId(id)})
    return jsonify({"mensagem": "Ocorrência excluída."})

# ✅ ROTA PARA ATUALIZAR OBSERVAÇÃO E MEDIDA
@app.route("/ocorrencias/<id>", methods=["PUT"])
def atualizar_ocorrencia(id):
    dados = request.json
    atualizacao = {}

    if "observacao" in dados:
        atualizacao["observacao"] = dados["observacao"]
    if "medidaProvidencia" in dados:
        atualizacao["medidaProvidencia"] = dados["medidaProvidencia"]

    resultado = colecao.update_one(
        {"_id": ObjectId(id)},
        {"$set": atualizacao}
    )

    if resultado.matched_count:
        return jsonify({"mensagem": "Ocorrência atualizada com sucesso."}), 200
    else:
        return jsonify({"erro": "Ocorrência não encontrada."}), 404

if __name__ == "__main__":
    app.run(debug=True)
