from flask import Blueprint, jsonify, request
from db import obtener_conexion_con_el_servidor
from herramientas import obtenerHabitacionDisponible

reservas_bp = Blueprint("reservas", __name__)

@reservas_bp.route("/agregar_reserva", methods=["POST"])
def agregar_reserva():
    
    conn = obtener_conexion_con_el_servidor()
    cursor = conn.cursor(dictionary=True, buffered=True) 

    data = request.get_json()

    print("Backend: data que llega del front para hacer una reserva: ", data)

    tipoHabitacion = data.get("tipoHabitacion")

    id_usuario = data.get("id_usuario")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    email = data.get("email")
    telefono = data.get("telefono")
    documento = data.get("dniPasaporte")
    ninios = data.get("ninios")
    adultos = data.get("adultos")
    fecha_entrada = data.get("fechaEntrada")
    fecha_salida = data.get("fechaSalida")

    habitacion_id = obtenerHabitacionDisponible(tipoHabitacion, fecha_entrada, fecha_salida, adultos, ninios, cursor)

    if not habitacion_id:
        return jsonify({"error": "No hay habitaciones de ese tipo disponibles"}), 409

    cursor.execute("""
                INSERT INTO reservas (id_usuario, nombre, apellido, email, telefono, documento, ninios, adultos, fecha_entrada, fecha_salida, habitacion_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (id_usuario, nombre, apellido, email, telefono, documento, ninios, adultos, fecha_entrada, fecha_salida, habitacion_id))
    conn.commit()

    cursor.close()
    conn.close()

    print("Backend: Reserva realizada y agregada correctamente")
    return ("Reserva agregada correctamente",200)

@reservas_bp.route("/listar_reservas/<idUsuario>", methods=["GET"])
def listar_reservas(idUsuario):

    conn = obtener_conexion_con_el_servidor()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM reservas WHERE id_usuario = %s",(idUsuario,))

    reserva = cursor.fetchall()

    cursor.close()
    conn.close()

    if not reserva:
        return jsonify({"mensaje": "No posees ninguna reserva"}), 404
    return jsonify(reserva)

@reservas_bp.route("/detalle/<int:id_reserva>", methods=["GET"])
def detalleReserva(id_reserva):

    conn = obtener_conexion_con_el_servidor()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM reservas WHERE id = %s", (id_reserva,))
    reserva = cursor.fetchone()

    cursor.close()
    conn.close()

    if not reserva:
        return jsonify({"mensaje": "Reserva no encontrada"}), 404

    return jsonify(reserva), 200

@reservas_bp.route("/<int:id_reserva>", methods=["GET"])
def obtener_reserva(id_reserva):

    conn = obtener_conexion_con_el_servidor()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM reservas WHERE id = %s", (id_reserva,))
    reserva = cursor.fetchone()

    cursor.close()
    conn.close()

    if not reserva:
        return jsonify({"mensaje": "Reserva no encontrada"}), 404

    return jsonify(reserva)

@reservas_bp.route("/borrar/<int:id_reserva>", methods=["DELETE"])
def borrar_reserva(id_reserva):

    conn = obtener_conexion_con_el_servidor()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM reservas WHERE id = %s", (id_reserva,))
    reserva = cursor.fetchone()

    if not reserva:
        cursor.close()
        conn.close()
        return jsonify({"error": "La reserva no existe"}), 404

    cursor.execute("DELETE FROM reservas WHERE id = %s", (id_reserva,))
    conn.commit()

    cursor.close()
    conn.close()

    print(f"Backend: Reserva con ID {id_reserva} eliminada correctamente.")

    return jsonify({"mensaje": "Reserva eliminada correctamente"}), 200