from flask import Blueprint, jsonify, request, render_template, request, redirect, url_for, flash, jsonify, session
from herramientas import estaLogeado
import requests
import os

cuenta_bp = Blueprint("cuenta", __name__)

@cuenta_bp.route("/cerrarSesion")
def cerrarSesion():
    print("Frontend: Cerrando la sesion: ", session["nombreUsuario"])
    session.clear()
    flash("Sesion cerrada correctamente.", "info")
    return redirect(url_for("index"))

@cuenta_bp.route("/miCuenta")
def miCuenta():
    if estaLogeado() is None:
        flash("Debes iniciar sesión para acceder a tu cuenta", "warning")
        return redirect(url_for('ingreso')) 
    
    dataUsuario = {
        "nombre": session.get("nombre"),
        "apellido": session.get("apellido"),
        "email": session.get("email"),
        "telefono": session.get("telefono"),
        "dniPasaporte": session.get("dniPasaporte"),
        "usuario": session.get("nombreUsuario"),
        "fechaCreacion": session.get("fechaCreacion")
    }

    return render_template('miCuenta.html', usuario=dataUsuario)

@cuenta_bp.route('/formularioDatos', methods=['GET', 'POST'])
def formularioDatos():

    if request.method == 'POST':
        datosPersonales = {
            "nombre": request.form["nombre"],
            "apellido": request.form["apellido"],
            "dniPasaporte": request.form["dniPasaporte"],
            "telefono": request.form["telefono"],
            "email": request.form["email"]
        }
        print("Datos personales: ", datosPersonales)
        return render_template('reserva.html', datosPersonales=datosPersonales)
    return render_template('formularioDatos.html')