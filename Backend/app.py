from flask import Flask, request, jsonify
from dotenv import load_dotenv
from mysql.connector import Error
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from flask import Flask
import mysql.connector
import os
from flask_cors import CORS
from routes.checkin import checkin_bp
from routes.clientes import clientes_bp
from routes.habitaciones import habitaciones_bp
from routes.reservas import reservas_bp
from routes.usuarios import usuarios_bp
from db import get_conection
from flask_mail import Mail
from herramientas import enviarMail

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

def create_app():

    iniciar_base_de_datos()
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(clientes_bp, url_prefix="/clientes")
    app.register_blueprint(habitaciones_bp, url_prefix="/habitaciones")
    app.register_blueprint(reservas_bp, url_prefix="/reservas")
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
    app.register_blueprint(checkin_bp, url_prefix="/check-in")

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

    mailCheckin = Mail(app)

    @app.route("/")
    def home():
        return "Flask se conectó a MariaDB correctamente!"
        
    return app