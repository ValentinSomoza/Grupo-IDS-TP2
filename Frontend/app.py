from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import json
import requests
app = Flask(__name__)

app.secret_key = 'texto-que-debe-existir' 

clientes = [] # Lista donde van los clientes temporal
BACKEND_URL = "http://127.0.0.1:5001/reservas"

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
            requests.post(BACKEND_URL, json=datosReserva)
            session.clear()
        except Exception as e:
            return f"Error de conexion con el backend: {e}"

    return render_template('reserva.html')

@app.route("/ingreso", methods=['GET', 'POST'])
def ingreso():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']

        for cliente in clientes:
            if cliente['usuario'] == usuario and cliente['contraseña'] == contraseña:
                flash (f' Bienvenido, {cliente["nombre"]} !')
                return redirect(url_for('index'))
        
        flash('Usuario o contraseña incorrectos')
        return redirect(url_for('ingreso'))
    return render_template('ingreso.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':

        nuevo_cliente = { # temporal
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'email': request.form['email'],
            'usuario': request.form['usuario'],
            'contraseña': request.form['contraseña']
        }

        for cliente in clientes:
            if cliente['usuario'] == nuevo_cliente['usuario']:
                flash('Ese nombre de usuario ya está registrado! Elige otro por favor')
                return redirect(url_for('registro'))
            if cliente['email'] == nuevo_cliente['email']:
                flash('Ese correo electrónico ya está registrado.')
                return redirect(url_for('registro'))

        clientes.append(nuevo_cliente) # temporal 
        flash('Usuario registrado con exito !') # temporal

        print(clientes) # verifico si se registro bien
        # aca se deberian guardar el usuario en la base de datos

        return redirect(url_for('registro'))
    return render_template('registro.html')

#clientes para el chechin
BACKEND_URL = "http://127.0.0.1:5001/"

#pida usuario, contraseña
idUsuario=int(1)
@app.route("/checkin")
def datosCheckin():
    response=requests.get(f"{BACKEND_URL}/cliente/{idUsuario}")
    datosUsuario=response.json()
    return render_template('check-inP1.html',datosUsuario=datosUsuario)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)