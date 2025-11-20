from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import json
import requests
from datetime import date
import base64
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")

@app.route("/")
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/galeria")
def galeria():
    imagenes = [
        'living1.jpg', 'living2.jpg', 'salon.jpg','ejecutivo.jpg' , 'bar.jpg', 
        'balcon.jpg', 'comedor.jpg', 'entrada.jpg', 'Baño 1.jpg', 'Baño 2.jpg',              
        'Dormitorio1.jpg', 'Dormitorio2.jpg', 
 ]
    return render_template("galeria.html", imagenes=imagenes)

@app.route("/mapa")
def mapa():
    return render_template('mapa.html')

def estaLogeado():
    nombreUsuario = request.args.get("nombreUsuario") or session.get("nombreUsuario")
    if not nombreUsuario:
        return None
    return nombreUsuario

@app.route("/eligeDatos")
def eligeDatos():
    if estaLogeado() is None:
        flash("⚠️ Debes iniciar sesión antes de hacer una reserva", "warning")
        return redirect(url_for('ingreso'))
    return render_template("eligeDatos.html")


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
        id_usuario = session.get("id")

        noches = request.form["noches"]
        adultos = request.form["adultos"]
        ninios = request.form["ninios"]
        tipoHabitacion = request.form["tipo-habitacion"]
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
            "fechaEntrada": fechaIngreso,
            "fechaSalida": fechaEgreso,
            "id_usuario": id_usuario
        }

        try: 
            respuesta = requests.post(f"{os.getenv('BACKEND_URL')}/reservas/agregar_reserva",json=datosReserva)
            print("Frontend: Reserva enviada al back: ", datosReserva)

            if respuesta.status_code != 200:
                info = respuesta.json()
                flash(info.get("error", "No se pudo realizar la reserva"), "error")
                return redirect(url_for("reserva"))

        except Exception as e:
            return f"Error de conexion con el backend: {e}"

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

@app.route("/completarDatosGoogle", methods=["GET", "POST"])
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

@app.route("/auth/callback/google", methods=['GET', 'POST'])
def google_auth():
    token = None

    if request.is_json:
        token = request.json.get("credential")
    if not token:
        token = request.args.get("credential")
    if not token:
        return jsonify({"status": "error", "mensaje": "Token no recibido"}), 400

    respuesta = requests.post(os.getenv("BACKEND_URL") + "/usuarios/authGoogle", json={"token": token})
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
                "redirect": url_for("completarDatosGoogle"),
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
            "redirect": url_for("ingreso"),
            "mensaje": info.get("error", "Error al iniciar sesion con Google")
        })

@app.route("/ingreso", methods=['GET', 'POST'])
def ingreso():
    if request.method == 'POST':

        usuarioIngresado = {
            'nombreUsuario': request.form['nombreUsuario'],
            'contrasenia': request.form['contrasenia']
        }

        print("Frontend: Nuevo ingreso de usuario enviado al backend: ", usuarioIngresado)

        respuesta = requests.post(os.getenv("BACKEND_URL") + "/usuarios/logearUsuario", json=usuarioIngresado)
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

@app.route('/registro', methods=['GET', 'POST'])
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
        
        respuesta = requests.post(os.getenv("BACKEND_URL") + "/usuarios/registrarUsuario", json=nuevoUsuario)
        info = respuesta.json()

        if respuesta.status_code == 200:
            flash(info.get("mensaje", "Registrado correctamente"), "success")
        elif respuesta.status_code == 409:
            flash(info.get("error", "Error en el registro"), "error")
        else:
            flash("Error inesperado al registrar usuario.", "error")

        print("Frontend: Nuevo registro de usuario enviado al backend: ", nuevoUsuario)

        return redirect(url_for('ingreso'))

    return render_template('registro.html')

@app.route("/checkin/<int:id_reserva>", methods=["GET", "POST"])
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
        
        response = requests.get(f"{os.getenv("BACKEND_URL")}/check-in/listar_reserva/{session.get("nombre")}")


        if response.status_code != 200:
            flash("Debes tener alguna reserva hecha antes de acceder al Check-In", "warning")
            return render_template('index.html') 


        response.raise_for_status()
        dataCheckin = response.json()

        print("Frontend: dataCheckin tiene actualmente: ", dataCheckin)
        return render_template('checkin.html', dataCheckin=dataCheckin[0])

    try: 
        requests.post(f"{os.getenv("BACKEND_URL")}/check-in/agregarCheckin", json=datosCheckin)
        print("Frontend: Checkin enviada al back: ", datosCheckin)
        flash("Check-in completado!", "success")

    except Exception as e:
        return f"Error de conexion con el backend: {e}"

    return redirect(url_for("index"))

@app.route("/cerrarSesion")
def cerrarSesion():
    print("Frontend: Cerrando la sesion: ", session["nombreUsuario"])
    session.clear()
    flash("Sesion cerrada correctamente.", "info")
    return redirect(url_for("index"))

@app.route("/miCuenta")
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

@app.route("/misReservas")
def misReservas():
    idUsuario = session.get("id")
    respuesta = requests.get(f"{os.getenv('BACKEND_URL')}/reservas/listar_reservas/{idUsuario}")

    if respuesta.status_code == 200:
            reservas = respuesta.json() 
            reservas = formatear_fechas(reservas)
    else:
        reservas = []

    return render_template('misReservas.html', reservas=reservas)

@app.route("/reserva/<int:id_reserva>")
def detalleReserva(id_reserva):
    respuesta = requests.get(f"{os.getenv('BACKEND_URL')}/reservas/detalle/{id_reserva}")

    if respuesta.status_code == 200:
        reserva = respuesta.json()
        formatear_fechas(reserva)

        pedirInfoHabitacion = requests.get(f"{os.getenv('BACKEND_URL')}/habitaciones/info/{reserva.get('habitacion_id')}")
        if pedirInfoHabitacion.status_code == 200:
            habitacion = pedirInfoHabitacion.json()
        else:
            habitacion = None 

        return render_template("detalleReserva.html", reserva=reserva, habitacion=habitacion)
    else:
        flash("No se encontró la reserva", "danger")
        return redirect(url_for("misReservas"))

@app.route("/reserva/checkin/<int:id_reserva>", methods=["POST"])
def redirigirCheckin(id_reserva):

    respuesta = requests.get(f"{os.getenv('BACKEND_URL')}/reservas/{id_reserva}")

    if respuesta.status_code != 200:
        flash("No se encontró la reserva", "error")
        return redirect(url_for("misReservas"))

    reserva = respuesta.json()

    if reserva.get("checkin") == 1 or reserva.get("checkin") is True:
        flash("Esta reserva ya tiene el Check-in realizado", "warning")
        return redirect(url_for("index"))

    return redirect(url_for("checkinPagina", id_reserva=id_reserva))

@app.route("/reserva/borrar/<int:id_reserva>", methods=["POST"]) # todavia falta implementar
def borrarReserva(id_reserva):
    respuesta = requests.delete(f"{os.getenv('BACKEND_URL')}/reservas/borrar/{id_reserva}")

    if respuesta.status_code == 200:
        flash("Reserva eliminada correctamente", "success")
    else:
        flash("Error al borrar la reserva", "danger")

    return redirect(url_for("misReservas"))

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

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)