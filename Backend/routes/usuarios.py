from flask import Blueprint, jsonify, request
from db import obtener_conexion_con_el_servidor
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
from flask_mail import Mail
from herramientas import enviarMail
import os

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("/logearUsuario", methods=["POST"])
def logearUsuario():
    usuarioIngresado = request.get_json() or {}

    nombreUsuario = usuarioIngresado.get("nombreUsuario")
    contrasenia = usuarioIngresado.get("contrasenia")

    conexion = obtener_conexion_con_el_servidor()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
    SELECT * FROM usuarios WHERE nombreUsuario = %s
    """, (nombreUsuario,))
    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    if not usuario:
        print("Backend: Usuario no encontrado en SQL: ", nombreUsuario)
        return jsonify({"error": "El usuario o la contraseña son incorrectos"}), 409

    if usuario["contrasenia"] != contrasenia:
        print("Backend: Contraseña incorrecta para el usuario: ", nombreUsuario)
        return jsonify({"error": "EL usuario o la contraseña son incorrectos"}), 409

    print("Backend: Ingreso de usuario exitoso para: ", usuarioIngresado)

    return jsonify({
        "mensaje": "Ingreso de sesion exitoso",
        "usuario": {
            "nombre": usuario["nombre"],
            "apellido": usuario["apellido"],
            "email": usuario["email"],
            "telefono": usuario["telefono"],
            "dniPasaporte": usuario["dniPasaporte"],
            "nombreUsuario": usuario["nombreUsuario"],
            "fechaCreacion": usuario["fechaCreacion"],
            "id":usuario["id"]
        }
    }), 200

@usuarios_bp.route("/registrarUsuario", methods=["POST"])
def registrarUsuario():
    nuevoUsuario = request.get_json()

    nombre = nuevoUsuario.get("nombre")
    apellido = nuevoUsuario.get("apellido")
    nombreUsuario = nuevoUsuario.get("nombreUsuario")
    email = nuevoUsuario.get("email")
    telefono = nuevoUsuario.get("telefono")
    dniPasaporte = nuevoUsuario.get("dniPasaporte")
    contrasenia = nuevoUsuario.get("contrasenia")

    conexion = obtener_conexion_con_el_servidor()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE nombreUsuario = %s", (nombreUsuario,))
    if cursor.fetchone():
        return jsonify({"error": "El usuario ya existe"}), 409

    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    if cursor.fetchone():
        return jsonify({"error": "El email ya esta registrado"}), 409 

    try:
        enviarMail(nuevoUsuario.get("email"), nuevoUsuario.get("nombre"), False)
    except Exception as e:
         print(e)
         return jsonify({"error": "El email ingresado es invalido"}), 409

    sql = """
    INSERT INTO usuarios (nombre, apellido, nombreUsuario, email, telefono, dniPasaporte, contrasenia)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (nombre, apellido, nombreUsuario, email, telefono, dniPasaporte, contrasenia))
    conexion.commit()

    cursor.close()
    conexion.close()

    print("Backend: Nuevo usuario registrado con exito:", nuevoUsuario)
    enviarMail(nuevoUsuario.get("email"), nuevoUsuario.get("nombre"), False)

    return jsonify({"mensaje": "Nuevo usuario registrado con exito !"}), 200

@usuarios_bp.route("/authGoogle", methods=["POST"])
def authGoogle():
    data = request.get_json() or {}
    token = data.get("token")

    if not token:
        return jsonify({"error": "Token no recibido"}), 400

    try:
        info = id_token.verify_oauth2_token(token, grequests.Request(), os.getenv('CLIENT_ID'))

        email = info.get("email")
        nombre = info.get("given_name") or ""
        apellido = info.get("family_name") or ""

        if not email:
            return jsonify({"error": "Email no provisto por Google"}), 400 # por si el servicio de google pifea

        conexion = obtener_conexion_con_el_servidor()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()

        if usuario: 
            cursor.close()
            conexion.close()
            return jsonify({
                "mensaje": "Inicio de sesion con Google exitoso",
                "usuario": {
                    "nombre": usuario["nombre"],
                    "apellido": usuario["apellido"],
                    "email": usuario["email"],
                    "telefono": usuario["telefono"],
                    "dniPasaporte": usuario["dniPasaporte"],
                    "nombreUsuario": usuario["nombreUsuario"],
                    "fechaCreacion": usuario["fechaCreacion"],
                    "id": usuario["id"]
                }
            }), 200

        nombreUsuarioNuevo = email
        cursor.execute("""
        INSERT INTO usuarios (nombre, apellido, email, nombreUsuario, telefono, dniPasaporte, contrasenia)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre, apellido, email, nombreUsuarioNuevo, None, None, None))

        conexion.commit()

        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        nuevoUsuario = cursor.fetchone()

        #enviarMail(email, nombre, False)

        cursor.close()
        conexion.close()

        respuestaNuevoUsuario = {
            "nombre": nuevoUsuario["nombre"],
            "apellido": nuevoUsuario["apellido"],
            "email": nuevoUsuario["email"],
            "telefono": nuevoUsuario["telefono"],
            "dniPasaporte": nuevoUsuario["dniPasaporte"],
            "nombreUsuario": nuevoUsuario["nombreUsuario"],
            "fechaCreacion": nuevoUsuario["fechaCreacion"],
            "id": nuevoUsuario["id"]
        }

        return jsonify({
            "mensaje": "Cuenta creada con Google e inicio de sesion exitoso",
            "usuario": respuestaNuevoUsuario
        }), 201

    except ValueError as e:
        print("Backend: ERROR en token Google: ", e)
        return jsonify({"error": "Token invalido"}), 400
    except Exception as e:
        print("Backend: ERROR inesperado en authGoogle: ", e)
        return jsonify({"error": "Error del servidor"}), 500

@usuarios_bp.route("/completarDatosGoogle", methods=["POST"])
def completarDatosGoogle():
    data = request.get_json() or {}
    email = data.get("email")
    telefono = data.get("telefono")
    dniPasaporte = data.get("dniPasaporte")

    if not email:
        return jsonify({"error": "Email es requerido y no fue enviado"}), 400

    conexion = obtener_conexion_con_el_servidor()
    cursor = conexion.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
    if cursor.fetchone() is None:
        cursor.close()
        conexion.close()
        return jsonify({"error": "Usuario no encontrado"}), 404

    cursor.execute("""
        UPDATE usuarios
        SET telefono = %s, dniPasaporte = %s
        WHERE email = %s
    """, (telefono, dniPasaporte, email))
    conexion.commit()

    cursor.close()
    conexion.close()

    print("Backend: Nuevos datos completados para el usuario de Google: ", email)
    return jsonify({"status": "ok", "mensaje": "Datos actualizados correctamente"}), 200