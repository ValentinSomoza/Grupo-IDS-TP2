from flask import Blueprint, jsonify, request, render_template, request, redirect, url_for, flash, jsonify, session
import requests
import os

registro_bp = Blueprint("registro", __name__)

@registro_bp.route('/registrarse', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':

        nuevoUsuario = { 
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'nombreUsuario': request.form['nombreUsuario'],
            'email': request.form['email'],
            'telefono':request.form['telefono'],
            'dniPasaporte':request.form['dniPasaporte'],
            'contrasenia': request.form['contrasenia']
        }
        
        respuesta = requests.post(f"{os.getenv("BACKEND_URL")}/usuarios/registrarUsuario", json=nuevoUsuario)
        info = respuesta.json()

        if respuesta.status_code == 200:
            flash(info.get("mensaje", "Registrado correctamente"), "success")
        elif respuesta.status_code == 409:
            flash(info.get("error", "Error en el registro"), "error")
        else:
            flash("Error inesperado al registrar usuario.", "error")

        print("Frontend: Nuevo registro de usuario enviado al backend: ", nuevoUsuario)

        return redirect(url_for('ingreso.ingreso'))

    return render_template('registro.html')