from flask import Blueprint, jsonify, request
from db import obtener_conexion_con_el_servidor
from herramientas import guardarImagenesDesdeFrontend, textoExiste, insertarTexto

datosIndex_bp = Blueprint("datosIndex", __name__)

@datosIndex_bp.route("/imagenesHotel", methods=["GET"])
def obtenerImagenesHotel():

    conexion = obtener_conexion_con_el_servidor()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT ruta FROM imagenes ORDER BY tipo ASC, orden ASC")
    resultados = cursor.fetchall()

    imagenes = [
        fila['ruta']
        for fila in resultados
        if "/personas/" not in fila['ruta'] and "\\personas\\" not in fila['ruta']
    ]

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

@datosIndex_bp.route("/cargar-imagenes", methods=["POST"])
def cargarImagenes():
    data = request.get_json()
    respuesta, status = guardarImagenesDesdeFrontend(data)
    return jsonify(respuesta), status

@datosIndex_bp.route("/cargar-textos", methods=["POST"])
def cargarTextos():
    dataDelFrontend = request.get_json()

    habitaciones = dataDelFrontend.get("habitaciones", [])
    servicios = dataDelFrontend.get("servicios", [])
    resenias = dataDelFrontend.get("resenias", [])

    conexion = obtener_conexion_con_el_servidor()
    cursor = conexion.cursor()

    totalHabitaciones = 0
    totalServicios = 0
    totalResenias = 0

    for habitacion in habitaciones:
        nombre = habitacion["nombre"]
        descripcion = habitacion["comentario"]

        if insertarTexto(cursor, "habitacion", nombre, descripcion):
            totalHabitaciones += 1

    for servicio in servicios:
        nombre = servicio["nombre"]
        descripcion = servicio["comentario"]

        if insertarTexto(cursor, "servicio", nombre, descripcion):
            totalServicios += 1

    for resenia in resenias:
        nombre = resenia["nombre"]
        descripcion = resenia["comentario"]

        if insertarTexto(cursor, "resenia", nombre, descripcion):
            totalResenias += 1

    conexion.commit()
    cursor.close()
    conexion.close()

    totalNombres = totalHabitaciones + totalServicios + totalResenias
    totalComentarios = totalNombres

    print("Backend: Se insertaron: ", totalNombres + totalComentarios, " textos a la base de datos")

    return jsonify({
        "mensaje": "Textos cargados correctamente a la base de datos",
        "total_nombres": totalNombres,
        "total_comentarios": totalComentarios
    })