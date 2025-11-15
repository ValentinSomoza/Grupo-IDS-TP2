from flask import Flask, request, jsonify
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
import os

app = Flask(__name__)

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

def create_app():

    app = Flask(__name__)

    reservas = [] # TEMPORAL
    clientes = [] # TEMPORAL

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
            if cliente["nombreUsuario"] == nuevoUsuario["nombreUsuario"]:
                return jsonify({"error": "El usuario ya existe !"}), 409
            if cliente["email"] == nuevoUsuario["email"]:
                return jsonify({"error": "El email ya está registrado"}), 409

        clientes.append(nuevoUsuario)

        print("Backend: Nuevo usuario registrado con exito:", nuevoUsuario)

        return jsonify({"mensaje": "Nuevo usuario registrado con exito !"}), 200

    return app