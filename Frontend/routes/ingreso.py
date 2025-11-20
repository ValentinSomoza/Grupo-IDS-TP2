from flask import Blueprint, jsonify, request, render_template, request, redirect, url_for, flash, jsonify, session
from herramientas import estaLogeado
import requests
import os


ingreso_bp = Blueprint("ingreso", __name__)



@ingreso_bp.route("/ingresar", methods=['GET', 'POST'])
def ingreso():
    if request.method == 'POST':

        usuarioIngresado = {
            'nombreUsuario': request.form['nombreUsuario'],
            'contrasenia': request.form['contrasenia']
        }

        print("Frontend: Nuevo ingreso de usuario enviado al backend: ", usuarioIngresado)
        print(os.getenv("BACKEND_URL"))
        respuesta = requests.post(f"{os.getenv("BACKEND_URL")}/usuarios/logearUsuario", json=usuarioIngresado)
        info = respuesta.json()

        if respuesta.status_code == 200:
            flash(info.get("mensaje", "Inicio de sesion exitoso"), "success")
            session['nombreUsuario'] = usuarioIngresado['nombreUsuario']
            usuario = info.get("usuario", {})
            
            session['logueado'] = True
            session['nombreUsuario'] = usuario.get("nombreUsuario")
            session['nombre'] = usuario.get("nombre")
            session['apellido'] = usuario.get("apellido")
            session['email'] = usuario.get("email")
            session['telefono'] = usuario.get("telefono")
            session['dniPasaporte'] = usuario.get("dniPasaporte")
            session['fechaCreacion'] = usuario.get("fechaCreacion")
            session['id'] = usuario.get("id")

            print("Frontend: Datos de sesión guardados correctamente:", session)
            return redirect(url_for('index'))

        elif respuesta.status_code == 409:
            flash(info.get("error", "Error al iniciar sesion"), "error")
        else:
            flash("Error inesperado al iniciar sesion. Por favor intente nuevamente.", "error")

        return redirect(url_for('ingreso'))
    return render_template('ingreso.html')
