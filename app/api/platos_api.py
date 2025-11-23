from flask import Blueprint, jsonify
from app.models import Plato

platos_api = Blueprint("platos_api", __name__)

@platos_api.route("/platos")
def get_platos():
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
