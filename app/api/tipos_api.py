from flask import Blueprint, jsonify
from app.models import TipoComida

tipos_api = Blueprint("tipos_api", __name__)

@tipos_api.route("/tipos")
def get_tipos():
    tipos = TipoComida.query.all()

    data = [
        {
            "id": t.id,
            "nombre": t.nombre
        }
        for t in tipos
    ]

    return jsonify(data)
