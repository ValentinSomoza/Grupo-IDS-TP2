from flask import Blueprint, jsonify, request
from db import obtener_conexion_con_el_servidor
from datetime import date
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
    index_textos = dataDelFrontend.get("index", [])

    conexion = obtener_conexion_con_el_servidor()
    cursor = conexion.cursor()

    totalHabitaciones = 0
    totalServicios = 0
    totalResenias = 0
    totalIndex = 0

    for item in index_textos:
        nombre = item["nombre"]
        descripcion = item["comentario"]

        if insertarTexto(cursor, "index", nombre, descripcion):
            totalIndex += 1

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

    totalNombres = totalHabitaciones + totalServicios + totalResenias + totalIndex
    totalComentarios = totalNombres

    print("Backend: Se insertaron: ", totalNombres + totalComentarios, " textos a la base de datos")

    return jsonify({
        "mensaje": "Textos cargados correctamente a la base de datos",
        "total_nombres": totalNombres,
        "total_comentarios": totalComentarios
    })

@datosIndex_bp.route("/textos", methods=["GET"])
def obtenerTextos():
    conexion = obtener_conexion_con_el_servidor()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT tipo, nombre, descripcion, orden FROM textos ORDER BY tipo ASC, orden ASC")
    filas = cursor.fetchall()

    cursor.close()
    conexion.close()

    textosPorTipo = {
        "habitacion": [],
        "servicio": [],
        "resenia": [],
        "index": []
    }

    for fila in filas:
        tipo = fila["tipo"]
        if tipo not in textosPorTipo:
            textosPorTipo[tipo] = []
        textosPorTipo[tipo].append({
            "nombre": fila["nombre"],
            "descripcion": fila["descripcion"]
        })

    return jsonify(textosPorTipo)

@datosIndex_bp.route("/habitaciones", methods=["GET"])
def obtenerHabitaciones():
    conexion = obtener_conexion_con_el_servidor()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT numero, tipo, capacidad, precio FROM habitaciones ORDER BY id ASC")
    habitaciones = cursor.fetchall()

    cursor.close()
    conexion.close()

    return jsonify(habitaciones)

@datosIndex_bp.route("/stats", methods=["GET"])
def obtenerStats():
    conexion = obtener_conexion_con_el_servidor()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM habitaciones")
    habitaciones = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM reservas WHERE checkin=1")
    personas_satisfechas = cursor.fetchone()["total"]

    cursor.close()
    conexion.close()

    return jsonify({
        "habitaciones": habitaciones,
        "personas_satisfechas": personas_satisfechas
    })

@datosIndex_bp.route("/habitaciones-disponibles", methods=["GET"])
def obtenerHabitacionesDisponiblesHoy():
    conexion = obtener_conexion_con_el_servidor()
    cursor = conexion.cursor(dictionary=True)

    hoy = date.today()

    cursor.execute("SELECT COUNT(*) AS total FROM habitaciones")
    totalHabitaciones = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(DISTINCT r.habitacion_id) AS ocupadas
        FROM reservas r
        WHERE r.fecha_entrada <= %s
        AND r.fecha_salida >= %s
    """, (hoy, hoy))
    habitacionesOcupadas = cursor.fetchone()["ocupadas"] or 0

    habitacionesDisponibles = totalHabitaciones - habitacionesOcupadas

    cursor.close()
    conexion.close()

    return jsonify({
        "habitacionesDisponibles": habitacionesDisponibles
    })