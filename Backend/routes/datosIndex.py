from flask import Blueprint, jsonify, request
from db import obtener_conexion_con_el_servidor

datosIndex_bp = Blueprint("datosIndex", __name__)

@datosIndex_bp.route("/imagenesHotel", methods=["GET"])
def obtenerTodasLasImagenes():

    conexion = obtener_conexion_con_el_servidor()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT ruta FROM imagenes ORDER BY tipo ASC, orden ASC")
    resultados = cursor.fetchall()

    imagenes = [fila['ruta'] for fila in resultados]

    cursor.close()
    conexion.close()

    return jsonify(imagenes)

@datosIndex_bp.route("/imagenesIndex", methods=["GET"])
def obtenerImagenesIndex():
    conexion = obtener_conexion_con_el_servidor()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT tipo, ruta FROM imagenes ORDER BY tipo ASC, orden ASC")
    resultados = cursor.fetchall()

    imagenesPorTipo = {}
    for fila in resultados:
        tipo = fila['tipo']
        ruta = fila['ruta']
        if tipo not in imagenesPorTipo:
            imagenesPorTipo[tipo] = []
        imagenesPorTipo[tipo].append(ruta)

    cursor.close()
    conexion.close()

    return jsonify(imagenesPorTipo)