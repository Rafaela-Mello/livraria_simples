from decimal import Decimal

from flask import flash, redirect, render_template, session, url_for

from app.database import fetch_all, fetch_one
from app.utils import is_logged_in


def register(app):
    @app.route("/historico")
    @app.route("/historico/<int:compra_id>")
    def historico(compra_id=None):
        if not is_logged_in():
            flash("Faça login para ver o histórico.", "erro")
            return redirect(url_for("login"))

        compras = fetch_all(
            """
            SELECT c.id, c.total, c.data_compra, COUNT(ic.id) AS qtd_itens
            FROM compras c
            LEFT JOIN itens_compra ic ON ic.compra_id = c.id
            WHERE c.usuario_id = %s
            GROUP BY c.id, c.total, c.data_compra
            ORDER BY c.data_compra DESC
            """,
            (session["usuario_id"],),
        )

        total_gasto = sum(Decimal(str(c["total"])) for c in compras)

        if not compra_id and compras:
            compra_id = compras[0]["id"]

        compra_detalhe = None
        itens_detalhe = []
        if compra_id:
            compra_detalhe = fetch_one(
                "SELECT id, total, data_compra FROM compras WHERE id = %s AND usuario_id = %s",
                (compra_id, session["usuario_id"]),
            )
            if compra_detalhe:
                itens_detalhe = fetch_all(
                    """
                    SELECT ic.quantidade, ic.preco_unitario, p.nome
                    FROM itens_compra ic
                    JOIN produtos p ON p.id = ic.produto_id
                    WHERE ic.compra_id = %s
                    """,
                    (compra_id,),
                )

        return render_template(
            "historico.html",
            compras=compras,
            compra_detalhe=compra_detalhe,
            itens_detalhe=itens_detalhe,
            total_gasto=total_gasto,
            qtd_compras=len(compras),
        )
