from flask import Blueprint, jsonify, request
from db import obtener_conexion_con_el_servidor

datosIndex_bp = Blueprint("datosIndex", __name__)

@datosIndex_bp.route("/imagenes", methods=["GET"])
def obtener_imagenes():
    conn = obtener_conexion_con_el_servidor()
    cursor = conn.cursor()

    cursor.execute("SELECT path FROM galeria ORDER BY id ASC")
    filas = cursor.fetchall()

    cursor.close()
    conn.close()

    imagenes = [
        f"{request.host_url}static/{fila[0]}"
        for fila in filas
    ]

    return jsonify(imagenes)