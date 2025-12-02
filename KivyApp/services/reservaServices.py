import os
import requests

def enviarReserva(datos):
    try:
        respuesta = requests.post(f"{os.getenv('BACKEND_URL')}/reservas/agregar_reserva", json=datos)

        if respuesta.status_code == 409:
            return {"error": respuesta.json().get("error", "No hay disponibilidad")}

        if respuesta.status_code != 200:
            return {"error": "Error al procesar la reserva"}

        return {"success": True}

    except Exception as e:
        return {"error": f"Error de conexión: {e}"}