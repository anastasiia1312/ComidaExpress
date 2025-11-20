from app.extensions import db
from flask_login import UserMixin
from app.extensions import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# usuarios

class User(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(50))


# tipoComida
class TipoComida(db.Model):
    __tablename__ = "tipo_comida"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), unique=True, nullable=False)

    restaurantes = db.relationship("Restaurant", backref="tipo_comida")


# restaurantes
class Restaurant(db.Model):
    __tablename__ = "restaurantes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(50))
    imagen_url = db.Column(db.String(255))
    calificacion = db.Column(db.Float, default=4.5)
    tiempo_entrega = db.Column(db.String(50))
    tipo_comida_id = db.Column(db.Integer, db.ForeignKey("tipo_comida.id"), nullable=False)

    platos = db.relationship("Plato", backref="restaurante")


# platos
class Plato(db.Model):
    __tablename__ = "platos"

    id = db.Column(db.Integer, primary_key=True)
    restaurante_id = db.Column(db.Integer, db.ForeignKey("restaurantes.id"), nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    imagen_url = db.Column(db.String(255))


#   pedidos
class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    restaurante_id = db.Column(db.Integer, db.ForeignKey("restaurantes.id"), nullable=False)
    direccion = db.Column(db.Text, nullable=False)

    total = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())
    estado = db.Column(db.String(50), default="pendiente")

    usuario = db.relationship("User", backref="pedidos")
    restaurante = db.relationship("Restaurant", backref="pedidos")
    detalles = db.relationship("PedidoDetalle", backref="pedido", cascade="all, delete")



# detallePedidios
class PedidoDetalle(db.Model):
    __tablename__ = "pedido_detalle"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    plato_id = db.Column(db.Integer, db.ForeignKey("platos.id"), nullable=False)

    cantidad = db.Column(db.Integer, nullable=False, default=1)
    precio = db.Column(db.Float, nullable=False)

    plato = db.relationship("Plato", backref="detalles")





