from .platos_api import platos_api
from .restaurantes_api import restaurantes_api
from .tipos_api import tipos_api

# lista de blueprints
apis = [
    platos_api,
    restaurantes_api,
    tipos_api
]
