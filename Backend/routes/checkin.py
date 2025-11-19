from flask import Blueprint, jsonify, request
from db import obtener_conexion_con_el_servidor


checkin_bp = Blueprint("check-in", __name__)

@checkin_bp.route("/agregarCheckin", methods=["POST"])
def agregarCheckin():

    conn = obtener_conexion_con_el_servidor()
    cursor = conn.cursor(dictionary=True)

    data = request.get_json()

    print("Backend: Check-in obtenido desde el formulario: ", data)

    nombre = data.get("nombre")
    apellido = data.get("apellido")
    dniPasaporte = data.get("dniPasaporte")
    telefono = data.get("telefono")
    emailUsuario = data.get("email")

    cursor.execute("""
                INSERT INTO checkin (nombre, apellido, email, dniPasaporte, telefono) 
                VALUES (%s, %s, %s, %s, %s)
                    """, (nombre, apellido, emailUsuario, dniPasaporte, telefono))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"mesanje": "Check-in completado, correo enviado"}), 200



@checkin_bp.route("/listar_reserva/<nombre>", methods=["GET"])
def listar_reserva(nombre):

    if not nombre:
        return jsonify({"mensaje": "No tienes ninguna reserva hecha"}), 404

    conn = obtener_conexion_con_el_servidor()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT nombre, apellido, documento, telefono, fecha_entrada, fecha_salida, email FROM reservas WHERE nombre= %s",(nombre,))


    reserva = cursor.fetchall()
    cursor.close()

    if not reserva:
        return jsonify({"mensaje": "No posees ninguna reserva"}), 404
    return jsonify(reserva)