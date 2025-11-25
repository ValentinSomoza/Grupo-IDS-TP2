from flask import Blueprint, jsonify, request
from db import obtener_conexion_con_el_servidor
from herramientas import enviarMail
from .reservas import detalleReserva

checkin_bp = Blueprint("check-in", __name__)

@checkin_bp.route("/agregarCheckin", methods=["POST"])
def agregarCheckin():

    data = request.get_json()
    id_reserva = data.get("id_reserva")
    nombreCheckin = data.get("nombre")
    apellidoCheckin = data.get("apellido")
    dniPasaporteCheckin = data.get("dniPasaporte")
    emailUsuario = data.get("email")

    print("Backend: Check-in obtenido desde el formulario: ", data)
    response, status_code = detalleReserva(id_reserva)

    if status_code == 200:
        dataBase = response.get_json()
        #comparacion con la base de datos
        if dataBase and (nombreCheckin == dataBase['nombre']) and (apellidoCheckin == dataBase['apellido']) and (dniPasaporteCheckin == dataBase['documento']):
            conn = obtener_conexion_con_el_servidor()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                UPDATE reservas SET checkin = TRUE WHERE id = %s
            """, (id_reserva,))
            conn.commit()
            cursor.close()
            conn.close()

            enviarMail(emailUsuario, nombreCheckin, dataBase) #envia el check-in
            return jsonify({"mensaje": "Check-in completado, correo enviado"}), 200
        else:
            return jsonify({"mensaje": "Los datos no coinciden con el titular!"}), 400
    else:
        return jsonify({"mensaje": "Reserva no encontrada"}), 404