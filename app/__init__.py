import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY")

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from app.models import (
            Restaurant, TipoComida, Plato,
            User, Pedido, PedidoDetalle
        )
        db.create_all()

    # blueprints
    from app.main.routes import main_bp
    from app.auth.routes import auth_bp
    from app.cart.routes import cart_bp
    from app.orders.routes import orders_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)

    from app.api.restaurantes_api import restaurantes_api
    from app.api.platos_api import platos_api
    from app.api.tipos_api import tipos_api

    app.register_blueprint(restaurantes_api, url_prefix="/api")
    app.register_blueprint(platos_api, url_prefix="/api")
    app.register_blueprint(tipos_api, url_prefix="/api")

    return app






