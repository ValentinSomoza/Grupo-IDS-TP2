from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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

@app.route("/reserva")
def reserva():
    return render_template('reserva.html')

@app.route("/reservar", methods=["POST"])
def reservar():
    fechaIngreso = request.form["fecha-entrada"]
    fechaEgreso = request.form["fecha-salida"]

    datosReserva = {
        "fechaEntrada": fechaIngreso,
        "fechaSalida": fechaEgreso
    }
    try: 
        respuesta = requests.post(BACKEND_URL, json=datosReserva)
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


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)