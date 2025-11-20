from flask import Blueprint, jsonify, request
from db import obtener_conexion_con_el_servidor

habitaciones_bp = Blueprint("Habitaciones", __name__)

@habitaciones_bp.route("/info/<habitacion_id>", methods=["GET"])
def info_habitacion(habitacion_id):

    conn = obtener_conexion_con_el_servidor()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM habitaciones WHERE id = %s
    """, (habitacion_id,))
    
    habitacion = cursor.fetchone()

    cursor.close()
    conn.close()

    if not habitacion:
        return jsonify({"mensaje": "Habitación no encontrada"}), 404

    return jsonify(habitacion), 200