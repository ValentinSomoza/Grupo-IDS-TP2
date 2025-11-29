from flask import Blueprint, jsonify, request, render_template, request, redirect, url_for, flash, jsonify, session
from herramientas import estaLogeado
import requests
import os

checkin_bp = Blueprint("checkin", __name__)

@checkin_bp.route("/<int:id_reserva>", methods=["GET", "POST"])
def checkinPagina(id_reserva):   
    if estaLogeado() is None:
        flash("Debes iniciar sesión antes de acceder al Check-In", "warning")
        return redirect(url_for('ingreso'))

    if request.method == 'POST':
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        documento = request.form["dniPasaporte"]
        emailUsuario = request.form["email"]
        telefono = request.form["telefono"]

        datosCheckin = {
            "nombre": nombre,
            "apellido": apellido,
            "dniPasaporte": documento,
            "telefono": telefono,
            "email": emailUsuario,
            "id_reserva": id_reserva
        }
    else:
        
        response = requests.get(f"{os.getenv('BACKEND_URL')}/reservas/detalle/{id_reserva}")

        if response.status_code != 200:
            flash("Debes tener alguna reserva hecha antes de acceder al Check-In", "warning")
            return render_template('index.html') 

        response.raise_for_status()
        dataCheckin = response.json()

        print("Frontend: dataCheckin tiene actualmente: ", dataCheckin)
        return render_template('checkin.html', dataCheckin=dataCheckin)

    try: 
        respBanckend = requests.post(f"{os.getenv('BACKEND_URL')}/check-in/validarCheckin", json=datosCheckin)
        print("Frontend: Checkin enviada al back: ", datosCheckin)
        mensajeBackend = respBanckend.json().get("mensaje", "respuesta")
        
        if respBanckend.status_code == 200:
            flash(mensajeBackend, "success")
        else:
            flash(mensajeBackend, "warning")

    except Exception as e:
        return f"Error de conexion con el backend: {e}"

    return redirect(url_for("index"))

@checkin_bp.route("/reserva/checkin/<int:id_reserva>", methods=["POST"])
def redirigirCheckin(id_reserva):

    respuesta = requests.get(f"{os.getenv('BACKEND_URL')}/reservas/{id_reserva}")

    if respuesta.status_code != 200:
        flash("No se encontró la reserva", "error")
        return redirect(url_for("misReservas"))

    reserva = respuesta.json()

    if reserva.get("checkin") == 1 or reserva.get("checkin") is True:
        flash("Esta reserva ya tiene el Check-in realizado", "warning")
        return redirect(url_for("index"))

    return redirect(url_for("checkin.checkinPagina", id_reserva=id_reserva))