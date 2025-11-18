from flask import Blueprint, jsonify, request
from db import get_server_conection

clientes_bp = Blueprint("clientes", __name__)

@clientes_bp.route("/")
def get_clientes(id_cliente):
    conn = get_server_conection()
    cursor = conn.cursor(dictionary=True)
    data = request.json
    nombre = data.get("Nombre")
    apellido = data.get("Apellido")
    email = data.get("Email")
    dni = data.get("Dni")
    fecha = data.get("Fecha")
    telefono = data.get("Telefono")
    cursor.execute("""
                INSERT INTO clientes (nombre, apellido, email, documento, fecha_registro, telefono) 
                VALUES (%s, %s, %s. %s, %s, %s)
                    """, (nombre,apellido,email,dni,fecha, telefono))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Cliente agregado correctamente")


@clientes_bp.route('/clientes', methods=['GET']) # A chequear
def ListaClientesBack():

    try:
        conexion = get_server_conection()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("USE HotelFAF")
        cursor.execute("SELECT * FROM clientes")
        listaClientes = cursor.fetchall()
        conexion.close()
        return jsonify({"mensaje": "Lista de clientes obtenida"}, listaClientes),200
    
    except Exception as e:
        print("Backend: Lista de clientes obtenida")
        return jsonify({"error": "No se pudo obtener datos del clientes desde la base de datos"}), 400

@clientes_bp.route('/cliente/<id>', methods=['GET']) # A chequear
def clientePorID(id):

    try:
        conexion = get_server_conection()
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

