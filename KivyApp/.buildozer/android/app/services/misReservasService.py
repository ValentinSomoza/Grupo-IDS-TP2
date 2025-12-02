import requests
import os

def obtenerReservas(id_usuario):
    try:
        url = f"{os.getenv('BACKEND_URL')}/reservas/listar_reservas/{id_usuario}"
        respuesta = requests.get(url)

        if respuesta.status_code == 200:
            return True, respuesta.json()

        elif respuesta.status_code == 404:
            return True, []  

        else:
            return False, "Error al obtener las reservas"

    except Exception as e:
        return False, f"Error inesperado de conexion: {e}"