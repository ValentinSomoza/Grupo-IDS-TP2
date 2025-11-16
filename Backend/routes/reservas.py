from flask import Blueprint, jsonify, request
from Backend.db import get_conection

reservas_bp = Blueprint("reservas", __name__)

@reservas_bp.route("/", methods=["POST"])
def add_reserva():
    #Tengo que corregir esto para que tome los datos del diccionario
    conn = get_conection()
    cursor = conn.cursor(dictionary=True)
    data = request.json
    print(data)
    nombre = data["nombre"]
    apellido = data["apellido"]
    email = data["email"]
    documento = data["dniPasaporte"]
    fecha_registro = data["fecha_registro"]
    telefono = data["telefono"]
    noches = data["noches"]
    ninios = data["niños"]
    adultos = data["adultos"]
    id_habitacion = data["numeroHabitacion"]
    fecha_entrada = data["fechaEntrada"]
    fecha_salida = data["fechaSalida"]
    cursor.execute("""
                INSERT INTO reservas (nombre, apellido, email, documento, fecha_registro, telefono,noches, ninios,adultos,id_habitacion,fecha_entrada,fecha_salida) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (nombre, apellido, email, documento, fecha_registro, int(telefono), noches, ninios, adultos,id_habitacion, fecha_entrada, fecha_salida))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Cliente agregado correctamente",200)