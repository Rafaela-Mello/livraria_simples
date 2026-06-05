from flask import flash, jsonify, redirect, render_template, request, session, url_for

from app.services.cart import cart_count, get_cart, get_cart_items, get_produto
from app.utils import is_logged_in, wants_json


def register(app):
    @app.route("/carrinho/adicionar/<int:produto_id>", methods=["POST"])
    def adicionar_carrinho(produto_id):
        if not is_logged_in():
            if wants_json():
                return jsonify({"success": False, "message": "Faça login para adicionar produtos."}), 401
            flash("Faça login para adicionar produtos ao carrinho.", "erro")
            return redirect(url_for("login"))

        produto = get_produto(produto_id)
        if not produto or produto["estoque"] <= 0:
            if wants_json():
                return jsonify({"success": False, "message": "Produto indisponível."}), 400
            flash("Produto indisponível.", "erro")
            return redirect(url_for("index", _anchor=f"produto-{produto_id}"))

        carrinho = get_cart()
        pid = str(produto_id)
        atual = carrinho.get(pid, 0)
        if atual >= produto["estoque"]:
            message = "Quantidade máxima em estoque atingida."
            if wants_json():
                return jsonify({"success": False, "message": message}), 400
            flash(message, "erro")
        else:
            carrinho[pid] = atual + 1
            session["carrinho"] = carrinho
            message = f"{produto['nome']} adicionado ao carrinho."
            if wants_json():
                items, total = get_cart_items()
                sidebar_html = render_template(
                    "_carrinho_sidebar.html",
                    items=items,
                    total=total,
                    cart_count=cart_count(),
                )
                return jsonify(
                    {
                        "success": True,
                        "message": message,
                        "cart_count": cart_count(),
                        "sidebar_html": sidebar_html,
                    }
                )
            flash(message, "sucesso")

        return redirect(url_for("index", _anchor=f"produto-{produto_id}"))

    @app.route("/carrinho")
    def carrinho():
        if not is_logged_in():
            flash("Faça login para acessar o carrinho.", "erro")
            return redirect(url_for("login"))

        items, total = get_cart_items()
        return render_template(
            "carrinho.html",
            items=items,
            total=total,
            usuario_nome=session.get("usuario_nome"),
            cart_count=cart_count(),
        )

    @app.route("/carrinho/aumentar/<int:produto_id>", methods=["POST"])
    def aumentar_carrinho(produto_id):
        if not is_logged_in():
            return redirect(url_for("login"))

        produto = get_produto(produto_id)
        carrinho = get_cart()
        pid = str(produto_id)

        if produto and pid in carrinho and carrinho[pid] < produto["estoque"]:
            carrinho[pid] += 1
            session["carrinho"] = carrinho
        else:
            flash("Não é possível aumentar: estoque insuficiente.", "erro")

        return redirect(url_for("carrinho"))

    @app.route("/carrinho/diminuir/<int:produto_id>", methods=["POST"])
    def diminuir_carrinho(produto_id):
        if not is_logged_in():
            return redirect(url_for("login"))

        carrinho = get_cart()
        pid = str(produto_id)
        if pid in carrinho:
            if carrinho[pid] > 1:
                carrinho[pid] -= 1
            else:
                del carrinho[pid]
            session["carrinho"] = carrinho

        return redirect(url_for("carrinho"))

    @app.route("/carrinho/remover/<int:produto_id>", methods=["POST"])
    def remover_carrinho(produto_id):
        if not is_logged_in():
            return redirect(url_for("login"))

        carrinho = get_cart()
        carrinho.pop(str(produto_id), None)
        session["carrinho"] = carrinho
        flash("Produto removido do carrinho.", "sucesso")
        return redirect(url_for("carrinho"))

    @app.route("/carrinho/limpar", methods=["POST"])
    def limpar_carrinho():
        if not is_logged_in():
            return redirect(url_for("login"))

        session["carrinho"] = {}
        flash("Carrinho esvaziado.", "sucesso")
        return redirect(url_for("carrinho"))
