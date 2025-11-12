from flask import Blueprint, jsonify, request
from db import get_conection

clientes_bp = Blueprint("Habitaciones", __name__)

@clientes_bp.route("/")
def get_clientes():
    conn = get_conection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("")
    
    pass


@clientes_bp.route("/#AGREGAR RUTA CORRESPONDIENTE")
def add_cliente_username():
    pass

@clientes_bp.route("/#AGREGAR RUTA CORRESPONDIENTE")
def add_cliente_password():
    pass
