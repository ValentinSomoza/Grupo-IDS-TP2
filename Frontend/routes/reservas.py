from flask import Blueprint, jsonify, request, render_template, request, redirect, url_for, flash, jsonify, session
import requests
import datetime
import os

reservas_bp = Blueprint("reservas", __name__)

@reservas_bp.route("/reserva", methods=['GET', 'POST'])
def reserva():

    if request.method == 'POST':

        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        dniPasaporte = request.form["dniPasaporte"]
        telefono = request.form["telefono"]
        email = request.form["email"]
        id_usuario = session.get("id")

        noches = request.form["noches"]
        adultos = request.form["adultos"]
        ninios = request.form["ninios"]
        tipoHabitacion = request.form["tipo-habitacion"]
        numeroHabitacion = request.form["numero-habitacion"]
        fechaIngreso = request.form["fecha-entrada"]
        fechaEgreso = request.form["fecha-salida"]

        datosReserva = {
            "nombre": nombre,
            "apellido": apellido,
            "dniPasaporte": dniPasaporte,
            "telefono": telefono,
            "email": email,
            "noches": noches,
            "adultos": adultos,
            "ninios": ninios,
            "tipoHabitacion": tipoHabitacion,
            "numeroHabitacion": numeroHabitacion,
            "fechaEntrada": fechaIngreso,
            "fechaSalida": fechaEgreso,
            "id_usuario": id_usuario
        }

        try: 
            requests.post(f"{os.getenv('BACKEND_URL')}/reservas/agregar_reserva",json=datosReserva)
        except Exception as e:
            return f"Error de conexion con el backend: {e}"

        print("Frontend: Reserva enviada al back: ", datosReserva)
        flash("Reserva realizada satisfactoriamente !", "success")
        return redirect(url_for("index"))

    datosPersonales = { 
        "nombre": session.get("nombre", ""),
        "apellido": session.get("apellido",""),
        "dniPasaporte": session.get("dniPasaporte", ""),
        "telefono": session.get("telefono", ""),
        "email": session.get("email", "")
    }
    return render_template('reserva.html', datosPersonales=datosPersonales)

@reservas_bp.route("/misReservas")
def misReservas():
    idUsuario = session.get("id")
    respuesta = requests.get(f"{os.getenv('BACKEND_URL')}/reservas/listar_reservas/{idUsuario}")

    if respuesta.status_code == 200:
            reservas = respuesta.json() 
            reservas = formatear_fechas(reservas)
    else:
        reservas = []

    return render_template('misReservas.html', reservas=reservas)


@reservas_bp.route("detalle_reservas/<int:id_reserva>")
def detalleReserva(id_reserva):
    respuesta = requests.get(f"{os.getenv('BACKEND_URL')}/reservas/detalle/{id_reserva}")

    if respuesta.status_code == 200:
        reserva = respuesta.json()
        reservas = formatear_fechas(reserva)
        return render_template("detalleReserva.html", reserva=reserva)
    else:
        flash("No se encontró la reserva", "danger")
        return redirect(url_for("misReservas"))


@reservas_bp.route("borrar_reserva/<int:id_reserva>", methods=["POST"]) # todavia falta implementar
def borrarReserva(id_reserva):
    respuesta = requests.delete(f"{os.getenv('BACKEND_URL')}/reservas/borrar/{id_reserva}")

    if respuesta.status_code == 200:
        flash("Reserva eliminada correctamente", "success")
    else:
        flash("Error al borrar la reserva", "danger")

    return redirect(url_for("reservas.misReservas"))

def formatear_fecha(fecha_str):
    try:
        fecha = datetime.strptime(fecha_str, "%a, %d %b %Y %H:%M:%S %Z")
        return fecha.strftime("%d/%m/%Y")
    except:
        return fecha_str

def formatear_fechas(reservas):
    if isinstance(reservas, dict):
        reservas["fecha_entrada"] = formatear_fecha(reservas["fecha_entrada"])
        reservas["fecha_salida"] = formatear_fecha(reservas["fecha_salida"])
        reservas["fecha_registro"] = formatear_fecha(reservas["fecha_registro"])

        return reservas
    else: 
        for reserva in reservas:
            if "fecha_entrada" in reserva:
                reserva["fecha_entrada"] = formatear_fecha(reserva["fecha_entrada"])
            if "fecha_salida" in reserva:
                reserva["fecha_salida"] = formatear_fecha(reserva["fecha_salida"])
            if "fecha_registro" in reserva:
                reserva["fecha_registro"] = formatear_fecha(reserva["fecha_registro"])
        return reservas






def formatear_fecha(fecha_str):
    try:
        fecha = datetime.strptime(fecha_str, "%a, %d %b %Y %H:%M:%S %Z")
        return fecha.strftime("%d/%m/%Y")
    except:
        return fecha_str

def formatear_fechas(reservas):
    if isinstance(reservas, dict):
        reservas["fecha_entrada"] = formatear_fecha(reservas["fecha_entrada"])
        reservas["fecha_salida"] = formatear_fecha(reservas["fecha_salida"])
        reservas["fecha_registro"] = formatear_fecha(reservas["fecha_registro"])

        return reservas
    else: 
        for reserva in reservas:
            if "fecha_entrada" in reserva:
                reserva["fecha_entrada"] = formatear_fecha(reserva["fecha_entrada"])
            if "fecha_salida" in reserva:
                reserva["fecha_salida"] = formatear_fecha(reserva["fecha_salida"])
            if "fecha_registro" in reserva:
                reserva["fecha_registro"] = formatear_fecha(reserva["fecha_registro"])
        return reservas

