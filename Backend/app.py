from flask import Flask, request, jsonify
from dotenv import load_dotenv
from mysql.connector import Error
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from flask import Flask
from flask_mail import Mail, Message
from email.mime.image import MIMEImage
import mysql.connector
import os
from flask_cors import CORS
from routes.clientes import clientes_bp
from routes.habitaciones import habitaciones_bp
from routes.reservas import reservas_bp
from routes.usuarios import usuarios_bp
from db import get_conection

CLIENT_ID = "826779228169-rpf8cnbbu9vue0gtfd2phi78tvn6sj0s.apps.googleusercontent.com"

def iniciar_base_de_datos():
    path = "db"
    path_absoluto = os.path.join(path,"init_db_prueba_juan.sql")
    with open(path_absoluto) as f:
        sql = f.read()
        print("Backend: SQL leido")

    conn = get_conection()
    cursor = conn.cursor()
    for statement in sql.split(";"):
        if statement.strip():
            cursor.execute(statement)
            conn.commit()
    cursor.close()
    conn.close()

mail = Mail()

def enviarMail(emailDestino, nombre):
    msg = Message(
        subject="Bienvenido!",
        recipients=[emailDestino]
    )

    msg.html = f"""
        <p>Hola <strong>{nombre}</strong>,</p>
        <h2>¡Registro exitoso!</h2>
        <img src="cid:logo_email" width="200">
        <p>¡Gracias por ser parte de <b>la Estancia Bruno Relax and Flask</b>!</p>
        <p>Estamos felices de tenerte con nosotros 🤗</p>
    """

    rutaLogo = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "Frontend", "static", "images", "LOGO.png")
    )

    with open(rutaLogo, "rb") as img:
        imagenData = img.read()

    msg.attach(
        filename="LOGO.png",
        content_type="image/png",
        data=imagenData,
        headers={"Content-ID": "<logo_email>"}
    )

    mail.send(msg)
    print("Backend: Se envió un email de bienvenida a:", emailDestino)

def create_app():

    iniciar_base_de_datos()
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(clientes_bp, url_prefix="/clientes")
    app.register_blueprint(habitaciones_bp, url_prefix="/habitaciones")
    app.register_blueprint(reservas_bp, url_prefix="/reservas")
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")

    clientes = [] # TEMPORAL

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

    mail.init_app(app)

    @app.route("/")
    def home():
        return "Flask se conectó a MariaDB correctamente!"
    
    @app.route("/logearUsuario", methods=["POST"])
    def logearUsuario():
        usuarioIngresado = request.get_json() or {}

        for cliente in clientes:
            if cliente.get("nombreUsuario") == usuarioIngresado.get("nombreUsuario") and cliente.get("contraseña") == usuarioIngresado.get("contraseña"):
                print("Backend: Ingreso de usuario exitoso: ", usuarioIngresado)
                
                return jsonify({
                    "mensaje": "Ingreso de sesion exitoso",
                    "usuario": {
                        "nombre": cliente.get("nombre"),
                        "apellido": cliente.get("apellido"),
                        "email": cliente.get("email"),
                        "telefono": cliente.get("telefono"),
                        "dniPasaporte": cliente.get("dniPasaporte"),
                        "nombreUsuario": cliente.get("nombreUsuario")
                    }
                }), 200

        print("Backend: Ingreso de usuario fallido: ", usuarioIngresado)
        return jsonify({"error": "El usuario o la contraseña son incorrectos"}), 409

    @app.route("/registrarUsuario", methods=["POST"])
    def registrarUsuario():
        nuevoUsuario = request.get_json()

        for cliente in clientes:
            if cliente.get("nombreUsuario") == nuevoUsuario.get("nombreUsuario"):
                return jsonify({"error": "El usuario ya existe !"}), 409
            if cliente.get("email") == nuevoUsuario.get("email"):
                return jsonify({"error": "El email ya está registrado"}), 409

        clientes.append(nuevoUsuario)

        print("Backend: Nuevo usuario registrado con exito:", nuevoUsuario)

        enviarMail(nuevoUsuario.get("email"), nuevoUsuario.get("nombre"))

        return jsonify({"mensaje": "Nuevo usuario registrado con exito !"}), 200

    @app.route("/authGoogle", methods=["POST"])
    def authGoogle():
        data = request.get_json() or {}
        token = data.get("token")

        try:
            info = id_token.verify_oauth2_token(token, grequests.Request(), CLIENT_ID)

            email = info["email"]
            nombre = info.get("given_name")
            apellido = info.get("family_name")

            for cliente in clientes:
                if cliente.get("email") == email:
                    print("Backend: Login con Google exitoso con el mail: ", email)

                    return jsonify({
                        "mensaje": "Inicio de sesión con Google exitoso",
                        "usuario": {
                            "nombre": cliente.get("nombre"),
                            "apellido": cliente.get("apellido"),
                            "email": cliente.get("email"),
                            "telefono": cliente.get("telefono"),
                            "dniPasaporte": cliente.get("dniPasaporte"),
                            "nombreUsuario": cliente.get("nombreUsuario")
                        }
                    }), 200

            nuevoCliente = {
                "nombre": nombre,
                "apellido": apellido,
                "email": email,
                "nombreUsuario": email,
                "telefono": None,
                "dniPasaporte": None,
                "contraseña": None
            }
            clientes.append(nuevoCliente)

            print("Backend: Usuario creado con Google: ", email)
            enviarMail(email, nombre)

            return jsonify({
                "mensaje": "Cuenta creada con Google e inicio de sesion exitoso",
                "usuario": nuevoCliente
            }), 200

        except Exception as e:
            print("Error en el Login con Google: ", str(e))
            return jsonify({"error": "Token invalido"}), 400

    @app.route('/clientes', methods=['GET'])
    def ListaClientesBack():

        try:
            conexion = conectarBaseDatos()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("USE HotelFAF")
            cursor.execute("SELECT * FROM clientes")
            listaClientes = cursor.fetchall()
            conexion.close()
            return jsonify({"mensaje": "Lista de clientes obtenida"}, listaClientes),200
        
        except Exception as e:
            print("Backend: Lista de clientes obtenida")
            return jsonify({"error": "No se pudo obtener datos del clientes desde la base de datos"}), 400

    @app.route('/cliente/<id>', methods=['GET'])
    def clientePorID(id):

        try:
            conexion = conectarBaseDatos()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("USE HotelFAF")
            cursor.execute(
                "SELECT nombre, apellido, email,fecha_registro, documento, telefono FROM clientes WHERE id = %s",(id,))
            clienteID = cursor.fetchall()
            conexion.close()
            print("Bacnkend: se obtuvo datos del usuario de la base de datos ")
            return jsonify(clienteID), 200
        
        except Exception as e:
            return jsonify({"error":"No se pudo obtener los datos del cliente desde la base de datos"})
   
    mailCheckin = Mail(app)

    @app.route("/checkinFormulario", methods=["POST"])
    def checkinFormulario():

        try:
            if request.method == "POST":

                nombre = request.form.get("nombre")
                apellido = request.form.get("apellido")
                documento = request.form.get("dniPasaporte")
                tipoHabitacion = request.form.get("tipo-habitacion")
                fechaEntrada = request.form.get("fecha-entrada")
                fechaSalida = request.form.get("fecha-salida")
                emailUsuario = request.form.get("email")
                telefono = request.form.get("telefono")
                print(f"El backend recibió un nuevo checkin:\n Nombre:{nombre}\n,Apellido:{apellido}") 

                emailEstancia = "estanciabruno@gmail.com" #gmail de la Estancia

                msg = Message(
                    "Check-in Estancia Bruno",
                    recipients=[emailUsuario, emailEstancia])
                
                msg.body = (
                    f"Estimado {nombre},\n"
                    f"Gracias por preferirnos, Estos son los detalles del checkin\n"
                    f"DATOS DEL TITULAR:\n"
                    f"Nombre: {nombre}, {apellido}\n"
                    f"Documento: {documento}\n"
                    f"Email: {emailUsuario}\n" 
                    f"Teléfono: {telefono}\n" 
                    f"ESTADIA:\n"
                    f"Habitacion: {tipoHabitacion}\n"
                    f"Fecha de entrada: {fechaEntrada}\n"
                    f"Fecha de salida: {fechaSalida}\n"
                )

                mailCheckin.send(msg)

                return jsonify({"mesanje": "Check-in completado, correo enviado"}), 200
            
        except Exception as e:
            return jsonify({"error": str(e), "mensaje":"No se completo el formulario"}), 400
        
    return app