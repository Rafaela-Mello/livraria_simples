from flask import flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app.database import execute, fetch_one


def register(app):
    @app.route("/cadastro", methods=["GET", "POST"])
    def cadastro():
        if request.method == "POST":
            nome = request.form.get("nome", "").strip()
            usuario = request.form.get("usuario", "").strip()
            senha = request.form.get("senha", "")
            confirmar = request.form.get("confirmar", "")

            if not nome or not usuario or not senha:
                flash("Preencha todos os campos.", "erro")
            elif senha != confirmar:
                flash("As senhas não coincidem.", "erro")
            elif fetch_one("SELECT id FROM usuarios WHERE usuario = %s", (usuario,)):
                flash("Usuário já cadastrado.", "erro")
            else:
                execute(
                    "INSERT INTO usuarios (nome, usuario, senha) VALUES (%s, %s, %s)",
                    (nome, usuario, generate_password_hash(senha)),
                )
                flash("Cadastro realizado com sucesso. Faça login.", "sucesso")
                return redirect(url_for("login"))

        return render_template("cadastro.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            usuario = request.form.get("usuario", "").strip()
            senha = request.form.get("senha", "")

            registro = fetch_one(
                "SELECT id, nome, usuario, senha FROM usuarios WHERE usuario = %s",
                (usuario,),
            )

            if registro and check_password_hash(registro["senha"], senha):
                session["usuario_id"] = registro["id"]
                session["usuario_nome"] = registro["nome"]
                session["usuario_login"] = registro["usuario"]
                flash(f"Bem-vindo(a), {registro['nome']}!", "sucesso")
                return redirect(url_for("index"))

            flash("Usuário ou senha inválidos.", "erro")

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Logout realizado com sucesso.", "sucesso")
        return redirect(url_for("index"))
