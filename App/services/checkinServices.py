import os
import requests

def realizarCheckin(idReserva, nombre, apellido, dniPasaporte, email, telefono):
    url = f"{os.getenv('BACKEND_URL')}/check-in/agregarCheckin"
    datosReserva = {
        "id_reserva": idReserva,
        "nombre": nombre,
        "apellido": apellido,
        "dniPasaporte": dniPasaporte,
        "email": email,
        "telefono": telefono
    }

    try:
        response = requests.post(url, json=datosReserva)

        if response.status_code == 200:
            return True, response.json().get("mensaje", "Check-in completado")

        else:
            return False, response.json().get("mensaje", "Error en el check-in")
            
    except Exception as e:
        return False, f"Error de conexión: {e}"