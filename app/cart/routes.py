from flask import Blueprint, session, jsonify
from app.models import Plato

cart_bp = Blueprint("cart", __name__)

def get_cart():
    return session.get("cart", {})

def save_cart(cart):
    session["cart"] = cart
    session.modified = True

def cart_total(cart):
    return sum(i["precio"] * i["cantidad"] for i in cart.values())

def add_item_to_cart(cart, plato_id):
    plato = Plato.query.get_or_404(plato_id)
    key = str(plato_id)

    item = cart.get(key, {
        "nombre": plato.nombre,
        "precio": plato.precio,
        "imagen": plato.imagen_url,
        "cantidad": 0,
    })
    item["cantidad"] += 1
    cart[key] = item
    return cart


@cart_bp.route("/add_to_cart/<int:plato_id>")
def add_to_cart(plato_id):
    if "user_id" not in session:
        return jsonify({"error": "login_required"}), 401

    cart = get_cart()
    add_item_to_cart(cart, plato_id)
    save_cart(cart)

    return jsonify({"success": True, "cart": cart, "total": cart_total(cart)})


@cart_bp.route("/cart_update/<int:plato_id>/<action>")
def cart_update(plato_id, action):
    cart = get_cart()
    key = str(plato_id)

    if action == "inc":
        add_item_to_cart(cart, plato_id)

    elif action == "dec":
        if key in cart:
            if cart[key]["cantidad"] > 1:
                cart[key]["cantidad"] -= 1
            else:
                del cart[key]

    save_cart(cart)
    return jsonify({"success": True, "cart": cart, "total": cart_total(cart)})


@cart_bp.route("/clear_cart")
def clear_cart():
    save_cart({})
    return jsonify({"success": True})


@cart_bp.route("/cart_state")
def cart_state():
    cart = get_cart()
    return jsonify({"cart": cart, "total": cart_total(cart)})
