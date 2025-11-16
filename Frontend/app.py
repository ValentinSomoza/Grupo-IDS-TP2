from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import json
import requests
import base64
app = Flask(__name__)

app.secret_key = 'texto-que-debe-existir' 
CLIENT_ID = "826779228169-rpf8cnbbu9vue0gtfd2phi78tvn6sj0s.apps.googleusercontent.com"
BACKEND_URL = "http://127.0.0.1:5001"

@app.route("/")
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/galeria")
def galeria():
    return render_template('galeria.html')

@app.route("/mapa")
def mapa():
    return render_template('mapa.html')

@app.route('/formularioDatos', methods=['GET', 'POST'])
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

@app.route("/reserva", methods=['GET', 'POST'])
def reserva():

    if request.method == 'POST':

        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        dniPasaporte = request.form["dniPasaporte"]
        telefono = request.form["telefono"]
        email = request.form["email"]

        noches = request.form["noches"]
        adultos = request.form["adultos"]
        niños = request.form["niños"]
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
            "niños": niños,
            "tipoHabitacion": tipoHabitacion,
            "numeroHabitacion": numeroHabitacion,
            "fechaEntrada": fechaIngreso,
            "fechaSalida": fechaEgreso,
            "fecha_registro": "2012-12-01"
        }


        try: 
            requests.post(f"{BACKEND_URL}/reservas/",json=datosReserva)
            session.clear()
        except Exception as e:
            return f"Error de conexion con el backend: {e}"

        flash("Reserva realizada satisfactoriamente !", "success")
        return redirect(url_for("index"))

    datosPersonales = {
        "nombre": "",
        "apellido": "",
        "dniPasaporte": "",
        "telefono": "",
        "email": ""
    }
    return render_template('reserva.html', datosPersonales=datosPersonales)

@app.route("/auth/callback/google", methods=['GET', 'POST'])
def google_auth():
    token = None

    if request.is_json:
        token = request.json.get("credential")
    if not token:
        token = request.args.get("credential")
    if not token:
        return jsonify({"status": "error", "mensaje": "Token no recibido"}), 400

    respuesta = requests.post(BACKEND_URL + "/authGoogle", json={"token": token})
    info = respuesta.json()

    print("Frontend: Ingreso de sesion con Google enviado al backend con el nombre: ", info.get("usuario", {}).get("nombre"))

    if respuesta.status_code in (200, 201):
        flash(info.get("mensaje", "Ingreso con google exitoso"), "success")

        usuario = info.get("usuario", {})
        session['logueado'] = True
        session['nombreUsuario'] = usuario.get("nombre") or usuario.get("email")
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
            "redirect": url_for("ingreso"),
            "mensaje": info.get("error", "Error al iniciar sesion con Google")
        })

@app.route("/ingreso", methods=['GET', 'POST'])
def ingreso():
    if request.method == 'POST':

        usuarioIngresado = {
            'nombreUsuario': request.form['nombreUsuario'],
            'contraseña': request.form['contraseña']
        }

        respuesta = requests.post(BACKEND_URL + "/logearUsuario", json=usuarioIngresado)
        info = respuesta.json()

        if respuesta.status_code == 200:
            flash(info.get("mensaje", "Inicio de sesion exitoso"), "success")
            session['nombreUsuario'] = usuarioIngresado['nombreUsuario']
            session['logueado'] = True
            return redirect(url_for('index'))
        elif respuesta.status_code == 409:
            flash(info.get("error", "Error al iniciar sesion"), "error")
        else:
            flash("Error inesperado al iniciar sesion. Por favor intente nuevamente.", "error")

        print("Frontend: Nuevo ingreso de usuario enviado al backend: ", usuarioIngresado)

        return redirect(url_for('ingreso'))
    return render_template('ingreso.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':

        nuevoUsuario = { 
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'nombreUsuario': request.form['nombreUsuario'],
            'email': request.form['email'],
            'contraseña': request.form['contraseña']
        }
        
        respuesta = requests.post(BACKEND_URL + "/registrarUsuario", json=nuevoUsuario)
        info = respuesta.json()

        if respuesta.status_code == 200:
            flash(info.get("mensaje", "Registrado correctamente"), "success")
        elif respuesta.status_code == 409:
            flash(info.get("error", "Error en el registro"), "error")
        else:
            flash("Error inesperado al registrar usuario.", "error")

        print("Frontend: Nuevo registro de usuario enviado al backend: ", nuevoUsuario)

        return redirect(url_for('index'))

    return render_template('registro.html')

@app.route("/checkin", methods=["GET"])
def checkinPagina():
    try:
        response=requests.get(f"{BACKEND_URL}/cliente/{idUsuario}")
        dataCheckin=response.json()

        return render_template('checkin.html', dataCheckin=dataCheckin)
    
    except Exception as e:
        return jsonify({"error":"Cliente no encontrado"})
       

@app.route("/checkinFinalizado")
def checkinFinalizadoPagina():
    return render_template('checkinFinalizado.html')

@app.route("/cerrarSesion") # No posee .html
def cerrarSesion():
    print("Frontend: Cerrando la sesion: ", session["nombreUsuario"])
    session.clear()
    flash("Sesion cerrada correctamente.", "info")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)