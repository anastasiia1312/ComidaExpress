from flask import Blueprint, redirect, url_for, session, request, render_template
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport.requests import Request
import os
from app.models import User
from app import db

auth_bp = Blueprint("auth", __name__)

# ENV
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:5000/auth/callback"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# GOOGLE FLOW 
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

# -------------------------
# LOGIN
# -------------------------
@auth_bp.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

# -------------------------
# CALLBACK
# -------------------------
@auth_bp.route("/callback")
def callback():
    if request.args.get("state") != session.get("state"):
        return render_template("error.html", message="El parámetro 'state' no coincide")

    try:
        flow.fetch_token(authorization_response=request.url)
    except:
        return render_template("error.html", message="Error al obtener el token")

    try:
        creds = flow.credentials
        id_info = id_token.verify_oauth2_token(
            creds.id_token,
            Request(),
            GOOGLE_CLIENT_ID
        )
    except:
        return render_template("error.html", message="Token inválido")

    email = id_info.get("email")
    name = id_info.get("name")

    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(
            nombre=name,
            email=email,
            contraseña="google_oauth"
        )
        db.session.add(user)
        db.session.commit()

    session["user_id"] = user.id

    return redirect(url_for("main.index"))

# -------------------------
# LOGOUT
# -------------------------
@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("main.index"))

