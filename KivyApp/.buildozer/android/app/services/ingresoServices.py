import requests
import os

def logearUsuario(nombreUsuario, contrasenia):
    url = f"{os.getenv('BACKEND_URL')}/usuarios/logearUsuario"
    datos = {"nombreUsuario": nombreUsuario, "contrasenia": contrasenia}

    try:
        respuesta = requests.post(url, json=datos)

        if respuesta.status_code == 200:
            return True, respuesta.json()
        else:
            mensaje_error = respuesta.json().get("error", "Error desconocido")
            return False, mensaje_error

    except Exception as e:
        return False, f"Error de conexión: {e}"