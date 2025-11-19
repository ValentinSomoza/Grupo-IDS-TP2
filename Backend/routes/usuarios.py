from flask import Blueprint, jsonify, request
from db import obtener_conexion_con_el_servidor
from app import grequests, id_token
from flask_mail import Mail
from herramientas import enviarMail
from constantes import CLIENT_ID

usuarios_bp = Blueprint("usuarios", __name__)
clientes = [] # TEMPORAL

pepe = { 
            'nombre': "pepe",
            'apellido': "mujica",
            'nombreUsuario': "pepe",
            'email': "vsomoza@fi.uba.ar",
            'telefono':"01234567890",
            'dniPasaporte':"01234567890",
            'contraseña': "mujica"
        }
        
clientes.append(pepe)



@usuarios_bp.route("/")
def add_usuario():
    conn = obtener_conexion_con_el_servidor()
    cursor = conn.cursor(dictionary=True)

    data = request.json
    usuario = data.get("usuario")
    email = data.get("email")
    contrasenia = data.get("contrasenia")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    cursor.execute("""
                INSERT INTO usuarios (usuario,email, contrasenia, nombre, apellido) 
                VALUES (%s, %s, %s. %s)
                    """, (usuario, email, contrasenia, nombre, apellido))
    conn.commit()
    cursor.close()
    conn.close()
    return ("usuario agregado correctamente")


@usuarios_bp.route("/logearUsuario", methods=["POST"])
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

@usuarios_bp.route("/registrarUsuario", methods=["POST"])
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


@usuarios_bp.route("/authGoogle", methods=["POST"])
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