from flask import Blueprint, jsonify, request
from Backend.db import get_conection

clientes_bp = Blueprint("clientes", __name__)

@clientes_bp.route("/")
def get_clientes(id_cliente):
    conn = get_conection()
    cursor = conn.cursor(dictionary=True)
    data = request.json
    nombre = data.get("Nombre")
    apellido = data.get("Apellido")
    email = data.get("Email")
    dni = data.get("Dni")
    fecha = data.get("Fecha")
    telefono = data.get("Telefono")
    cursor.execute("""
                INSERT INTO clientes (nombre, apellido, email, documento, fecha_registro, telefono) 
                VALUES (%s, %s, %s. %s, %s, %s)
                    """, (nombre,apellido,email,dni,fecha, telefono))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Cliente agregado correctamente")


@clientes_bp.route("/#AGREGAR RUTA CORRESPONDIENTE")
def add_cliente_username():
    pass

@clientes_bp.route("/#AGREGAR RUTA CORRESPONDIENTE")
def add_cliente_password():
    pass