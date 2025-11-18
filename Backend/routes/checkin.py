from flask import Blueprint, jsonify, request
from app import Message,mailCheckin


checkin_bp = Blueprint("check-in", __name__)

@checkin_bp.route("/checkinFormulario", methods=["POST"])
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

            mailCheckin.send(msg)

            return jsonify({"mesanje": "Check-in completado, correo enviado"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e), "mensaje":"No se completo el formulario"}), 400