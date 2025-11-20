from flask import Blueprint, render_template
from app.models import Restaurant, TipoComida 
from app.extensions import db

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    categories = TipoComida.query.all()

    restaurants = Restaurant.query.all()

    return render_template("index.html", categories=categories, restaurants=restaurants)
