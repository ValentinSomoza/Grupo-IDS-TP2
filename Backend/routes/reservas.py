from flask import Blueprint, jsonify, request
from db import obtener_conexion_con_el_servidor

reservas_bp = Blueprint("reservas", __name__)

@reservas_bp.route("/agregar_reserva", methods=["POST"])
def agregar_reserva():
    
    conn = obtener_conexion_con_el_servidor()
    cursor = conn.cursor(dictionary=True)

    data = request.get_json()

    print("Backend: data que llega del front para hacer una reserva: ", data)

    id_usuario = data.get("id_usuario")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    email = data.get("email")
    telefono = data.get("telefono")
    documento = data.get("dniPasaporte")
    noches = data.get("noches")
    ninios = data.get("niños")
    adultos = data.get("adultos")
    fecha_entrada = data.get("fechaEntrada")
    fecha_salida = data.get("fechaSalida")
    id_habitacion = data.get("numeroHabitacion")

    cursor.execute("""
                INSERT INTO reservas (id_usuario, nombre, apellido, email, telefono, documento, noches, ninios, adultos, fecha_entrada, fecha_salida, id_habitacion) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (id_usuario, nombre, apellido, email, telefono, documento, noches, ninios, adultos, fecha_entrada, fecha_salida, id_habitacion))
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
    print("Backend: se lista las siguientes reservas: ", reserva)

    cursor.close()
    conn.close()

    if not reserva:
        return jsonify({"mensaje": "No posees ninguna reserva"}), 404
    return jsonify(reserva)