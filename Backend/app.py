from flask import Flask, request, jsonify
from dotenv import load_dotenv
from mysql.connector import Error
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
import mysql.connector
import os
from flask_cors import CORS

from routes.checkin import checkin_bp
from routes.clientes import clientes_bp
from routes.habitaciones import habitaciones_bp
from routes.reservas import reservas_bp
from routes.usuarios import usuarios_bp

from db import obtener_conexion, obtener_conexion_con_el_servidor
from flask_mail import Mail
from herramientas import enviarMail
from init_data import crearUsuarioTest

load_dotenv()

def iniciarBaseDeDatos():

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS HotelBruno")

    cursor.close()
    conn.close()

    conn = obtener_conexion_con_el_servidor()
    cursor = conn.cursor()

    cursor.execute("SHOW TABLES LIKE 'habitaciones'")
    tablaExiste = cursor.fetchone()

    if tablaExiste:
        cursor.close()
        conn.close()
        return

    path = "db"
    path_absoluto = os.path.join(path, "init_db.sql")

    with open(path_absoluto) as f:
        sql = f.read()

    print("Backend: Ejecutando init_db.sql...")

    for statement in sql.split(";"):
        if statement.strip():
            cursor.execute(statement)
            conn.commit()

    cursor.close()
    conn.close()

def create_app():

    iniciarBaseDeDatos()

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

    crearUsuarioTest()

    @app.route("/")
    def home():
        return "Flask se conectó a SQL correctamente!"

    return app