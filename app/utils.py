from flask import request, session


def is_logged_in():
    return "usuario_id" in session


def wants_json():
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"
