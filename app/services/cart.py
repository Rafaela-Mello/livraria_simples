from decimal import Decimal

from flask import session

from app.database import fetch_all, fetch_one


def get_cart():
    return session.setdefault("carrinho", {})


def cart_count():
    return sum(get_cart().values())


def get_produto(produto_id):
    return fetch_one(
        "SELECT id, nome, descricao, preco, estoque FROM produtos WHERE id = %s",
        (produto_id,),
    )


def get_cart_items():
    carrinho = get_cart()
    if not carrinho:
        return [], Decimal("0")

    ids = list(carrinho.keys())
    placeholders = ", ".join(["%s"] * len(ids))
    produtos = fetch_all(
        f"SELECT id, nome, preco, estoque FROM produtos WHERE id IN ({placeholders})",
        tuple(int(i) for i in ids),
    )

    items = []
    total = Decimal("0")
    for produto in produtos:
        pid = str(produto["id"])
        quantidade = min(carrinho[pid], produto["estoque"])
        if quantidade <= 0:
            continue
        subtotal = Decimal(str(produto["preco"])) * quantidade
        items.append(
            {
                "id": produto["id"],
                "nome": produto["nome"],
                "preco": produto["preco"],
                "estoque": produto["estoque"],
                "quantidade": quantidade,
                "subtotal": subtotal,
            }
        )
        total += subtotal

    session["carrinho"] = {str(item["id"]): item["quantidade"] for item in items}
    return items, total
