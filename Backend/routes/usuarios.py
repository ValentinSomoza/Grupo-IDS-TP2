from flask import Blueprint, jsonify, request
from db import get_conection

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("/")
def add_usuario():
    conn = get_conection()
    cursor = conn.cursor(dictionary=True)
    data = request.json
    usuario = data.get("usuario")
    email = data.get("email")
    contrasenia = data.get("contrasenia")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    cursor.execute("""
                INSERT INTO usuarios (usuario,email, contrasenia, nombre, apellido) 
                VALUES (%s, %s, %s. %s)
                    """, (usuario, email, contrasenia, nombre, apellido))
    conn.commit()
    cursor.close()
    conn.close()
    return ("usuario agregado correctamente")