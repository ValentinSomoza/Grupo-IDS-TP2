from flask import request, session

def estaLogeado():
    nombreUsuario = request.args.get("nombreUsuario") or session.get("nombreUsuario")
    if not nombreUsuario:
        return None
    return nombreUsuario