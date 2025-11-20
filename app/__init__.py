from flask import Flask
from app.extensions import db, login_manager
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__)

    # SECRET KEY
    app.secret_key = os.getenv("FLASK_SECRET_KEY")

    # database config
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from app.models import Restaurant, TipoComida, Plato, User, Pedido, PedidoDetalle
        db.create_all()

    # register blueprints
    from app.auth.routes import main
    app.register_blueprint(main)

    return app









