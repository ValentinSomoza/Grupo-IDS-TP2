from flask import Flask, request, jsonify
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
import os

app = Flask(__name__)

load_dotenv()
def conectarBaseDatos():
    try: 
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS")
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

    reservas = []

    @app.route("/")
    def home():
        return "Flask se conectó a MariaDB correctamente!"

    iniciarBaseDeDatos()

    @app.route("/reservas", methods=["POST"])
    def recibirReserva():
        data = request.get_json()
        reservas.append(data)
        
        print("Nueva reserva: ", data)

        return jsonify({"mensaje": "Reserva guardada con exito !"}), 200

    return app

#endpoint listar todos los clientes
@app.route('/clientes', methods=['GET'])
def clientes():
    conexion = conectarBaseDatos()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("USE HotelFAF")
    cursor.execute("SELECT * FROM clientes")
    listaClientes = cursor.fetchall()
    conexion.close()
    return jsonify(listaClientes),200

#endpoint listar un nombre por id del cliente
@app.route('/cliente/<id>', methods=['GET'])
def cliente(id):
    conexion = conectarBaseDatos()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("USE HotelFAF")
    cursor.execute(
        "SELECT nombre, apellido, email,fecha_registro, documento FROM clientes WHERE id = %s",(id,))
    listaClientes = cursor.fetchall()
    conexion.close()
    return jsonify(listaClientes),200

#ccapturar datos del form


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)