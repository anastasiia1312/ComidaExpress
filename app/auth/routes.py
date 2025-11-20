from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google.auth.transport.requests
import os

from app.models import Restaurant, TipoComida, Plato, User, Pedido, PedidoDetalle
from app.extensions import db

main = Blueprint("main", __name__)

# google auth

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:5000/auth/callback"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

flow = Flow.from_client_config(
    {
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [REDIRECT_URI],
        }
    },
    scopes=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ],
    redirect_uri=REDIRECT_URI
)

# agregar plato en corrito

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


# index

@main.route("/")
def index():
    user = session.get("user")
    categories = TipoComida.query.all()

    selected = request.args.get("categoria")
    query = request.args.get("q", "").strip()

    if query:
        restaurants = Restaurant.query.filter(
            Restaurant.nombre.ilike(f"%{query}%")
        ).all()

        platos = Plato.query.filter(
            Plato.nombre.ilike(f"%{query}%")
        ).all()

        restaurant_ids = {p.restaurante_id for p in platos}

        restaurants += Restaurant.query.filter(
            Restaurant.id.in_(restaurant_ids)
        ).all()

        restaurants = list({r.id: r for r in restaurants}.values())

    else:
        if selected and selected != "all":
            cat = TipoComida.query.filter_by(nombre=selected).first()
            restaurants = Restaurant.query.filter_by(tipo_comida_id=cat.id).all() if cat else []
        else:
            restaurants = Restaurant.query.all()

    return render_template(
        "index.html",
        user=user,
        categories=categories,
        restaurants=restaurants,
        selected_category=selected,
        query=query
    )


# restaurantes

@main.route("/restaurant/<int:restaurant_id>")
def restaurant(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    platos = Plato.query.filter_by(restaurante_id=restaurant_id).all()
    return render_template("restaurantes.html", restaurant=restaurant, platos=platos)


# auth

@main.route("/login")
def login():
    url, state = flow.authorization_url()
    session["state"] = state
    return redirect(url)


@main.route("/auth/callback")
def callback():
    if request.args.get("state") != session.get("state"):
        return "Error state"

    flow.fetch_token(authorization_response=request.url)
    creds = flow.credentials

    try:
        info = id_token.verify_oauth2_token(
            creds.id_token,
            google.auth.transport.requests.Request(),
            GOOGLE_CLIENT_ID
        )
    except:
        return "erroro de token"

    email = info["email"]
    name = info.get("name")

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(nombre=name, email=email, contraseña="google_oauth")
        db.session.add(user)
        db.session.commit()

    session["user"] = {
        "id": user.id,
        "email": user.email,
        "name": user.nombre,
        "picture": info.get("picture")
    }

    return redirect(url_for("main.index"))


@main.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("main.index"))


# carrito

@main.route("/add_to_cart/<int:plato_id>")
def add_to_cart(plato_id):
    if "user" not in session:
        return jsonify({"error": "login_required"}), 401

    cart = get_cart()
    add_item_to_cart(cart, plato_id)
    save_cart(cart)

    return jsonify({"success": True, "cart": cart, "total": cart_total(cart)})


@main.route("/cart_update/<int:plato_id>/<action>")
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


@main.route("/clear_cart")
def clear_cart():
    save_cart({})
    return jsonify({"success": True})

@main.route("/cart_state")
def cart_state():
    cart = get_cart()
    return jsonify({
        "cart": cart,
        "total": cart_total(cart)
    })



# pedido

@main.route("/checkout")
def checkout():
    cart = get_cart()
    if not cart:
        return redirect(url_for("main.index"))

    return render_template("checkout.html", cart=cart, total=cart_total(cart))


@main.route("/make_order", methods=["POST"])
def make_order():
    if "user" not in session:
        return redirect(url_for("main.login"))

    cart = get_cart()
    if not cart:
        return redirect(url_for("main.index"))

    user_id = session["user"]["id"]

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

