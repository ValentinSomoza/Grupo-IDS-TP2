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
from Backend.routes.clientes import clientes_bp
from Backend.routes.habitaciones import habitaciones_bp
from Backend.routes.reservas import reservas_bp
from Backend.routes.usuarios import usuarios_bp
#from Backend.routes.usuarios import usuarios_bp


def conectarBaseDatos():
    try: 
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
        )
    except Error as e:
        print("Error al conectar con la base de datos ", e)
        return None



def iniciarBaseDeDatos():
    try:
        conexion = conectarBaseDatos()

        if conexion.is_connected():
            cursor = conexion.cursor()

            sql_path = os.path.join(os.path.dirname(__file__), "db", "init_db.sql")

            with open(sql_path, "r") as f:
                sql_script = f.read()
            
            for statement in sql_script.split(";"):
                stmt = statement.strip()
                if stmt:
                    cursor.execute(stmt)
            
            conexion.commit()
            print("Base de datos inicializada !")
    
    except Error as e:
        print("Base de datos no pudo inicializarse debido al error ", e)
    
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


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

    app = Flask(__name__)

    CORS(app)
    #No estoy seguro de que esos prefix sean correctos, cualquier cosa despues los cambiamos
    app.register_blueprint(clientes_bp, url_prefix="/clientes")
    app.register_blueprint(habitaciones_bp, url_prefix="/habitaciones")
    app.register_blueprint(reservas_bp, url_prefix="/reservas")
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")


    reservas = [] # TEMPORAL
    clientes = [] # TEMPORAL
    CLIENT_ID = "826779228169-rpf8cnbbu9vue0gtfd2phi78tvn6sj0s.apps.googleusercontent.com"

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

    iniciarBaseDeDatos()

    @app.route("/recibirReserva", methods=["POST"])
    def recibirReserva():
        data = request.get_json()
        reservas.append(data) # TEMPORAL 
        
        print("Nueva reserva: ", data)

        return jsonify({"mensaje": "Reserva guardada con exito !"}), 200
    
    @app.route("/logearUsuario", methods=["POST"])
    def logearUsuario():
        usuarioIngresado = request.get_json() or {}

        for cliente in clientes:
            if cliente.get("nombreUsuario") == usuarioIngresado.get("nombreUsuario") and cliente.get("contraseña") == usuarioIngresado.get("contraseña"):
                print("Backend: Ingreso de usuario exitoso: ", usuarioIngresado)
                return jsonify({"mensaje": "Ingreso de sesion exitoso"}), 200

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
                    return jsonify({"mensaje": "Inicio de sesion exitoso con Google"}), 200

            nuevoCliente = {
                "nombre": nombre,
                "apellido": apellido,
                "email": email,
                "nombreUsuario": email,
                "contraseña": None
            }
            clientes.append(nuevoCliente)

            print("Backend: Usuario creado con Google: ", email)
            enviarMail(email, nombre)

            return jsonify({"mensaje": "Cuenta creada con Google e inicio exitoso"}), 200

        except Exception as e:
            print("Error en el Login con Google: ", str(e))
            return jsonify({"error": "Token invalido"}), 400

    return app