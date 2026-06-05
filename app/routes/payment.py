from flask import flash, redirect, render_template, request, session, url_for

from app.database import execute, execute_many
from app.services.cart import cart_count, get_cart_items
from app.utils import is_logged_in


def finalizar_compra(items, total):
    usuario_id = session["usuario_id"]
    compra_id = execute(
        "INSERT INTO compras (usuario_id, total) VALUES (%s, %s)",
        (usuario_id, total),
    )

    queries = []
    for item in items:
        queries.append(
            (
                "INSERT INTO itens_compra (compra_id, produto_id, quantidade, preco_unitario) "
                "VALUES (%s, %s, %s, %s)",
                (compra_id, item["id"], item["quantidade"], item["preco"]),
            )
        )
        queries.append(
            (
                "UPDATE produtos SET estoque = estoque - %s WHERE id = %s",
                (item["quantidade"], item["id"]),
            )
        )

    execute_many(queries)
    return compra_id


def register(app):
    @app.route("/pagamento", methods=["GET", "POST"])
    def pagamento():
        if not is_logged_in():
            flash("Faça login para finalizar a compra.", "erro")
            return redirect(url_for("login"))

        items, total = get_cart_items()
        if not items:
            flash("Seu carrinho está vazio.", "erro")
            return redirect(url_for("carrinho"))

        if request.method == "POST":
            numero = request.form.get("numero", "").replace(" ", "")
            nome = request.form.get("nome_titular", "").strip()
            validade = request.form.get("validade", "").strip()
            cvv = request.form.get("cvv", "").strip()

            if len(numero) < 13 or not nome or not validade or len(cvv) < 3:
                flash("Dados do cartão inválidos.", "erro")
            else:
                compra_id = finalizar_compra(items, total)
                session["carrinho"] = {}
                flash("Pagamento aprovado! Compra finalizada.", "sucesso")
                return redirect(url_for("historico", compra_id=compra_id))

        return render_template(
            "pagamento.html",
            items=items,
            total=total,
            usuario_nome=session.get("usuario_nome"),
            cart_count=cart_count(),
        )
