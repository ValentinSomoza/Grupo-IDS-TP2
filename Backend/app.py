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

    return app