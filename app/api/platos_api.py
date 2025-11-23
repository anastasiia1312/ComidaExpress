import os, json
from flask import Blueprint, jsonify
from app.models import Plato

platos_api = Blueprint("platos_api", __name__)

JSON_PATH = "platos.json"

@platos_api.route("/platos")
def get_platos():

    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, encoding="utf-8") as f:
            return jsonify(json.load(f))

    platos = Plato.query.all()

    data = [
        {
            "id": p.id,
            "nombre": p.nombre,
            "descripcion": p.descripcion,
            "precio": p.precio,
            "imagen_url": p.imagen_url,
            "restaurante_id": p.restaurante_id
        }
        for p in platos
    ]

    return jsonify(data)

