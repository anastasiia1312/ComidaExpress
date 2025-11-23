from flask import Blueprint, render_template, request
from app.models import Restaurant, TipoComida, Plato

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    categories = TipoComida.query.all()

    selected = request.args.get("categoria")
    query = request.args.get("q", "").strip()

    # busqueda por restourantes o platos
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

        # eliminar duplicados
        restaurants = list({r.id: r for r in restaurants}.values())

    # filtro por categoria
    else:
        if selected and selected != "all":
            cat = TipoComida.query.filter_by(nombre=selected).first()
            restaurants = Restaurant.query.filter_by(
                tipo_comida_id=cat.id
            ).all() if cat else []
        else:
            restaurants = Restaurant.query.all()

    return render_template(
        "index.html",
        categories=categories,
        restaurants=restaurants,
        selected_category=selected,
        query=query
    )

@main_bp.route("/restaurant/<int:restaurant_id>")
def restaurant(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    platos = Plato.query.filter_by(restaurante_id=restaurant_id).all()
    return render_template("restaurantes.html", restaurant=restaurant, platos=platos)

