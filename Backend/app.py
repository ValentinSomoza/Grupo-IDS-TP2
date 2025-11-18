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
from Backend.routes.checkin import checkin_bp
#from Backend.routes.usuarios import usuarios_bp
from Backend.db import get_conection



def init_db():
    path = "db"
    path_absoluto = os.path.join(path,"init_db_prueba_juan.sql")
    with open(path_absoluto) as f:
        sql = f.read()

        conn = get_conection()
        cursor = conn.cursor()
        for statement in sql.split(";"):
            if statement.strip():
                cursor.execute(statement)
                conn.commit()
                print("Sentencia ejecutada")
        cursor.close()
        conn.close()

init_db()

def conectarBaseDatos():
    try: 
        return mysql.connector.connect(
            host="mysql",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")  # opcional si definís DB_NAME en .env
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
            cursor.close()
            conexion.close()
    
    except Error as e:
        print("Base de datos no pudo inicializarse debido al error ", e)
    
    #finally:
        #if conexion.is_connected():
        
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
    app.register_blueprint(clientes_bp, url_prefix="/clientes")
    app.register_blueprint(habitaciones_bp, url_prefix="/habitaciones")
    app.register_blueprint(reservas_bp, url_prefix="/reservas")
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
    app.register_blueprint(checkin_bp,url_prefix="/check-in")

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

    #iniciarBaseDeDatos()
    mailCheckin = Mail(app)
        
    return app