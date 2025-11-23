import os, json
from flask import Blueprint, jsonify
from app.models import TipoComida

tipos_api = Blueprint("tipos_api", __name__)

JSON_PATH = "tipo_comida.json"

@tipos_api.route("/tipos")
def get_tipos():

    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, encoding="utf-8") as f:
            return jsonify(json.load(f))

    tipos = TipoComida.query.all()

    data = [
        {
            "id": t.id,
            "nombre": t.nombre
        }
        for t in tipos
    ]

    return jsonify(data)

