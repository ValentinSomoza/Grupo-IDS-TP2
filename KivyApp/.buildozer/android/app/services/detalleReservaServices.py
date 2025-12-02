import requests
import os

def obtenerDetalleReserva(id_reserva):
    try:
        respuesta = requests.get(f"{os.getenv('BACKEND_URL')}/reservas/detalle/{id_reserva}")
        if respuesta.status_code == 200:
            return True, respuesta.json()
        return False, None
    except Exception as e:
        print("Error al obtener la reserva:", e)
        return False, None

def obtenerInfoHabitacion(habitacion_id):
    if not habitacion_id:
        return False, None
    try:
        respuesta = requests.get(f"{os.getenv('BACKEND_URL')}/habitaciones/info/{habitacion_id}")
        if respuesta.status_code == 200:
            return True, respuesta.json()
        return False, None
    except Exception as e:
        print("Error al obtener info de habitación:", e)
        return False, None

def borrarReserva(id_reserva):
    try:
        respuesta = requests.delete(f"{os.getenv('BACKEND_URL')}/reservas/borrar/{id_reserva}")
        if respuesta.status_code == 200:
            return True
        return False
    except Exception as e:
        print("Error al borrar la reserva:", e)
        return False