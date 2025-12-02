import requests
import os
from dotenv import load_dotenv

load_dotenv()

def registrarUsuario(nombre, apellido, nombreUsuario, email, telefono, dniPasaporte, contrasenia):

    peticion = f"{os.getenv('BACKEND_URL')}/usuarios/registrarUsuario"
    datos = {
        "nombre": nombre,
        "apellido": apellido,
        "nombreUsuario": nombreUsuario,
        "email": email,
        "telefono": telefono,
        "dniPasaporte": dniPasaporte,
        "contrasenia": contrasenia
    }

    try:
        respuesta = requests.post(peticion, json=datos)

        if respuesta.status_code == 200: # devuelve una tupla
            return True, respuesta.json()
        else:
            mensaje_error = respuesta.json().get("error", "Error desconocido")
            return False, mensaje_error

    except Exception as e:
        return False, f"Error de conexión: {e}"