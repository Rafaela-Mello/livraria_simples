from decimal import Decimal

from flask import render_template

from app.database import fetch_all
from app.services.cart import cart_count, get_cart_items
from app.utils import is_logged_in


def register(app):
    @app.route("/")
    def index():
        produtos = fetch_all(
            "SELECT id, nome, descricao, preco, estoque FROM produtos ORDER BY nome"
        )
        items, total = get_cart_items() if is_logged_in() else ([], Decimal("0"))
        return render_template(
            "index.html",
            produtos=produtos,
            logado=is_logged_in(),
            items=items,
            total=total,
        )
