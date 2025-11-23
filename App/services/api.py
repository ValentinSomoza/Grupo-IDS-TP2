import requests
import os

def login_usuario(nombre, contrasenia):
    try:
        respuesta = requests.post(
            f"{os.getenv('BACKEND_URL')}/usuarios/logearUsuario",
            json={"nombreUsuario": nombre, "contrasenia": contrasenia}
        )

        if respuesta.status_code == 200:
            return True, respuesta.json().get("mensaje", "Ingreso exitoso")

        return False, respuesta.json().get("error", "Error en el login")

    except Exception as e:
        return False, f"Error inesperado: {str(e)}"