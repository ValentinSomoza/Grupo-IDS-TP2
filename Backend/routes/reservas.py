from flask import Blueprint, jsonify, request
from db import get_conection

reservas_bp = Blueprint("reservas", __name__)

@reservas_bp.route("/")
def add_reserva(id_cliente):
    conn = get_conection()
    cursor = conn.cursor(dictionary=True)
    data = request.json
    id_habitacion = data.get("id_habitacion")
    fecha_entrada = data.get("fecha_entrada")
    fecha_salida = data.get("fecha_salida")
    cursor.execute("""
                INSERT INTO reservas (nombre, apellido, email, documento, fecha_registro, telefono) 
                VALUES (%s, %s, %s. %s)
                    """, (id_cliente, id_habitacion, fecha_entrada, fecha_salida))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Cliente agregado correctamente")

