from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import requests
app = Flask(__name__)

app.secret_key = 'texto-que-debe-existir' 

CLIENT_ID = "826779228169-rpf8cnbbu9vue0gtfd2phi78tvn6sj0s.apps.googleusercontent.com"

clientes = [] # TEMPORAL
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
        session['nombre'] = request.form["nombre"]
        session['apellido'] = request.form["apellido"]
        session['dniPasaporte'] = request.form["dni-pasaporte"]
        session['telefono'] = request.form["telefono"]
        session['email'] = request.form["email"]
        print("Datos personales recibidos: ", session)

        return redirect(url_for('reserva'))

    return render_template('formularioDatos.html')

@app.route("/reserva", methods=['GET', 'POST'])
def reserva():

    if request.method == 'POST':

        nombre = session.get('nombre')
        apellido = session.get("apellido")
        dniPasaporte = session.get("dniPasaporte")
        telefono = session.get("telefono")
        email = session.get("email")

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
            "fechaSalida": fechaEgreso
        }

        try: 
            requests.post(BACKEND_URL + "/recibirReserva", json=datosReserva)
            session.clear()
        except Exception as e:
            return f"Error de conexion con el backend: {e}"

    return render_template('reserva.html')

@app.route("/auth/callback/google", methods=["POST"])
def google_auth():
    token = request.json.get("credential")

    respuesta = requests.post(BACKEND_URL + "/authGoogle", json={"token": token})
    info = respuesta.json()

    print("Ingreso de sesion con Google enviado al backend")

    if respuesta.status_code in (200, 201):
        flash(info.get("mensaje", "Ingreso con google exitoso"), "success")
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

        return redirect(url_for('registro'))

    return render_template('registro.html')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)