from flask import Flask, session

from app.config import SECRET_KEY
from app.routes import register_routes
from app.services.cart import cart_count


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    @app.context_processor
    def inject_globals():
        return {
            "usuario_nome": session.get("usuario_nome"),
            "cart_count": cart_count(),
        }

    register_routes(app)
    return app
