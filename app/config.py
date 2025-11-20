import os
from decouple import config

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = config("SECRET_KEY", default="dev_key_123")  
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, '..', 'instance', 'database.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
