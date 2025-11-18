from flask import Blueprint, jsonify, request
from db import get_server_conection


checkin_bp = Blueprint("check-in", __name__)

@checkin_bp.route('/clientes', methods=['GET']) # A chequear
def ListaClientesBack():
    try:
        conexion = get_server_conection()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes")
        listaClientes = cursor.fetchall()
        conexion.close()
        return jsonify({"mensaje": "Lista de clientes obtenida"}, listaClientes),200
    
    except Exception as e:
        print("Backend: Lista de clientes obtenida")
        return jsonify({"error": "No se pudo obtener datos del clientes desde la base de datos"}), 400

@checkin_bp.route('/cliente/<id>', methods=['GET']) # A chequear
def clientePorID(id):

    try:
        conexion = get_server_conection()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("USE HotelFAF")
        cursor.execute(
            "SELECT nombre, apellido, email,fecha_registro, documento, telefono FROM clientes WHERE id = %s",(id,))
        clienteID = cursor.fetchall()
        conexion.close()
        print("Bacnkend: se obtuvo datos del usuario de la base de datos ")
        return jsonify(clienteID), 200
    
    except Exception as e:
        return jsonify({"error":"No se pudo obtener los datos del cliente desde la base de datos"})


@checkin_bp.route("/checkinFormulario", methods=["POST"]) # falta modularizar
def checkinFormulario():

    try:
        if request.method == "POST":

            nombre = request.form.get("nombre")
            apellido = request.form.get("apellido")
            documento = request.form.get("dniPasaporte")
            tipoHabitacion = request.form.get("tipo-habitacion")
            fechaEntrada = request.form.get("fecha-entrada")
            fechaSalida = request.form.get("fecha-salida")
            emailUsuario = request.form.get("email")
            telefono = request.form.get("telefono")
            print(f"El backend recibió un nuevo checkin:\n Nombre:{nombre}\n,Apellido:{apellido}") 

            emailEstancia = "estanciabruno@gmail.com" #gmail de la Estancia

            msg = Message(
                "Check-in Estancia Bruno",
                recipients=[emailUsuario, emailEstancia])
            
            msg.body = (
                f"Estimado {nombre},\n"
                f"Gracias por preferirnos, Estos son los detalles del checkin\n"
                f"DATOS DEL TITULAR:\n"
                f"Nombre: {nombre}, {apellido}\n"
                f"Documento: {documento}\n"
                f"Email: {emailUsuario}\n" 
                f"Teléfono: {telefono}\n" 
                f"ESTADIA:\n"
                f"Habitacion: {tipoHabitacion}\n"
                f"Fecha de entrada: {fechaEntrada}\n"
                f"Fecha de salida: {fechaSalida}\n"
            )

            mailCheckin.send(msg) # Capaz se rompe en esta linea porque el mailCheckin esta en el app

            return jsonify({"mesanje": "Check-in completado, correo enviado"}), 200


    except Exception as e:
        return jsonify({"error": str(e), "mensaje":"No se completo el formulario"}), 400  

@checkin_bp.route("/listar_reserva/<nombre>", methods=["GET"])
def listar_reserva(nombre):

    conn = get_server_conection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT nombre, apellido, documento, telefono, fecha_entrada, fecha_salida, email FROM reservas WHERE nombre= %s",(nombre,))


    reserva = cursor.fetchall()
    cursor.close()
    
    if not reserva:
        return jsonify({"mensaje": "No posees ninguna reserva"}), 404
    return jsonify(reserva)