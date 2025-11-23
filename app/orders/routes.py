from flask import Blueprint, render_template, redirect, url_for, session, request
from app.models import Plato, Pedido, PedidoDetalle
from app import db

orders_bp = Blueprint("orders", __name__)

from app.cart.routes import get_cart, cart_total, save_cart


@orders_bp.route("/checkout")
def checkout():
    cart = get_cart()
    if not cart:
        return redirect(url_for("main.index"))
    return render_template("checkout.html", cart=cart, total=cart_total(cart))


@orders_bp.route("/make_order", methods=["POST"])
def make_order():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    cart = get_cart()
    if not cart:
        return redirect(url_for("main.index"))

    user_id = session["user_id"]

    direccion = f"{request.form.get('ciudad')}, {request.form.get('calle')} {request.form.get('altura')}, Piso {request.form.get('piso')}, Depto {request.form.get('departamento')}"

    primer = Plato.query.get(int(next(iter(cart))))
    restaurante_id = primer.restaurante_id

    total = cart_total(cart)

    pedido = Pedido(
        usuario_id=user_id,
        restaurante_id=restaurante_id,
        direccion=direccion,
        total=total,
        estado="pendiente"
    )
    db.session.add(pedido)
    db.session.commit()

    for plato_id, item in cart.items():
        detalle = PedidoDetalle(
            pedido_id=pedido.id,
            plato_id=int(plato_id),
            cantidad=item["cantidad"],
            precio=item["precio"]
        )
        db.session.add(detalle)

    db.session.commit()

    save_cart({})

    return render_template("success.html", pedido_id=pedido.id)
