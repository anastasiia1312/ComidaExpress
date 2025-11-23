import os, json
from flask import Blueprint, jsonify
from app.models import Restaurant

restaurantes_api = Blueprint("restaurantes_api", __name__)

JSON_PATH = "restaurantes.json"

@restaurantes_api.route("/restaurants")
def get_restaurants():

    # Render
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, encoding="utf-8") as f:
            return jsonify(json.load(f))

    # local
    restaurantes = Restaurant.query.all()

    data = [
        {
            "id": r.id,
            "nombre": r.nombre,
            "telefono": r.telefono,
            "imagen_url": r.imagen_url,
            "calificacion": r.calificacion,
            "tiempo_entrega": r.tiempo_entrega,
            "tipo": r.tipo_comida.nombre if r.tipo_comida else None
        }
        for r in restaurantes
    ]

    return jsonify(data)

