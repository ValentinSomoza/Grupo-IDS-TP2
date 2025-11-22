from flask import Blueprint, jsonify, request, render_template, request, redirect, url_for, flash, jsonify, session
from herramientas import estaLogeado
import requests
import os

autenticacion_bp = Blueprint("autenticacion", __name__)

@autenticacion_bp.route("/completarDatosGoogle", methods=["GET", "POST"])
def completarDatosGoogle():
    if request.method == "POST":
        telefono = request.form.get("telefono")
        dniPasaporte = request.form.get("dniPasaporte")

        session["telefono"] = telefono
        session["dniPasaporte"] = dniPasaporte

        try:
            requests.post(
                os.getenv("BACKEND_URL") + "/usuarios/completarDatosGoogle",
                json={
                    "email": session["email"],
                    "telefono": telefono,
                    "dniPasaporte": dniPasaporte
                }
            )
        except:
            flash("Error conectando con el backend", "error")

        flash("Datos completados correctamente", "success")
        print("Frontend: Datos para la cuenta de Google completados correctamente")
        return redirect(url_for("index"))

    return render_template("completarDatosGoogle.html")

@autenticacion_bp.route("/auth/callback/google", methods=['POST'])
def google_auth():
    token = None

    if request.is_json:
        token = request.json.get("credential")
    if not token:
        token = request.args.get("credential")
    if not token:
        return jsonify({"status": "error", "mensaje": "Token no recibido"}), 400

    respuesta = requests.post(os.getenv('BACKEND_URL') + "/usuarios/authGoogle", json={"token": token})
    info = respuesta.json()

    print("Frontend: Ingreso de sesion con Google enviado al backend con el nombre: ", info.get("usuario", {}).get("nombre"))

    if respuesta.status_code in (200, 201):
        flash(info.get("mensaje", "Ingreso con google exitoso"), "success")

        usuario = info.get("usuario", {})
        session['logueado'] = True
        session['nombreUsuario'] = usuario.get("nombre") or usuario.get("email")
        session['nombre'] = usuario.get("nombre")
        session['apellido'] = usuario.get("apellido")
        session['email'] = usuario.get("email")
        session['telefono'] = usuario.get("telefono")
        session['dniPasaporte'] = usuario.get("dniPasaporte")
        session['fechaCreacion'] = usuario.get("fechaCreacion")
        session['id'] = usuario.get("id")

        if session.get("telefono") is None or session.get("dniPasaporte") is None:
            print("Frontend: El usuario se logeo con google y posee sus datos incompletos")
            return jsonify({
                "status": "ok",
                "redirect": url_for("autenticacion.completarDatosGoogle"),
                "mensaje": info.get("mensaje", "Ingreso con Google exitoso con datos incompletos")
            })
        
        print("Frontend: Usuario: ", session.get("nombreUsuario"), " logeado correctamente")
        return jsonify({
            "status": "ok",
            "redirect": url_for("index"),
            "mensaje": info.get("mensaje", "Ingreso con Google exitoso")
        })
    else:
        flash(info.get("error", "Error al iniciar sesion con Google"), "error")
        return jsonify({
            "status": "error",
            "redirect": url_for("ingreso.ingreso"),
            "mensaje": info.get("error", "Error al iniciar sesion con Google")
        })
