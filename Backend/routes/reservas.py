from flask import Blueprint, jsonify, request
from db import get_server_conection

reservas_bp = Blueprint("reservas", __name__)

@reservas_bp.route("/agregar_reserva", methods=["POST"])
def agregar_reserva():
    
    conn = get_server_conection()
    cursor = conn.cursor(dictionary=True)

    data = request.get_json()

    print("Backend: data que llega del front: ", data)

    nombre = data.get("nombre")

    apellido = data.get("apellido")
    email = data.get("email")
    documento = data.get("dniPasaporte")
    fecha_registro = data.get("fecha_registro")
    telefono = data.get("telefono")
    noches = data.get("noches")
    ninios = data.get("niños")
    adultos = data.get("adultos")
    id_habitacion = data.get("numeroHabitacion")
    fecha_entrada = data.get("fechaEntrada")
    fecha_salida = data.get("fechaSalida")


    cursor.execute("""
                INSERT INTO reservas (nombre, apellido, email, documento, fecha_registro, telefono, noches, ninios, adultos, id_habitacion, fecha_entrada, fecha_salida) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (nombre, apellido, email, documento, fecha_registro, telefono, noches, ninios, adultos,id_habitacion, fecha_entrada, fecha_salida))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Cliente agregado correctamente",200)

@reservas_bp.route("/listar_reservas/<int:dni>", methods=["GET"])
def listar_reservas(dni):

    """Funcion que lista reservas de un DNI"""

    conn = get_server_conection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reservas WHERE documento = %s",(dni,))

    reserva = cursor.fetchall()
    print("Backend: se lista las siguientes reservas: ", reserva)
    cursor.close()
    conn.commit()

    if not reserva:
        return jsonify({"mensaje": "No posees ninguna reserva"}), 404
    return jsonify(reserva)