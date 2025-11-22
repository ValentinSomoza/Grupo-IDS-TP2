from flask_mail import Mail, Message
from email.mime.image import MIMEImage
import os

def enviarMail(emailDestino, nombre, esCheckin):
    
    rutaLogo = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "Frontend", "static", "images", "LOGO.png")
    )

    with open(rutaLogo, "rb") as img:
        imagenData = img.read()

    if isinstance(esCheckin, dict):
        
        msg = Message(
            subject="Chenck-in Hotel Bruno!",
            recipients=[emailDestino]
        )
        msg.html = f"""
            <p>Hola <strong>{nombre}</strong>,</p>
            <h2>¡Te confirmamos que tú check-in ha sido registrado!</h2>
            <h3>Detalle de tú registro:</h3>

            <p>Nombre:{esCheckin['nombre']} {esCheckin['apellido']}</p>
            <p>DNI:{esCheckin['documento']}</p>
            <p>Fecha de entrada:{esCheckin['fecha_entrada']}</p>
            <p>Fecha de salida:{esCheckin['fecha_salida']}</p>
            <p>Id de la reserva:{esCheckin['id']}</p>
            <p>Id de habitación:{esCheckin['habitacion_id']}</p>

            <img src="cid:logo_email" width="200">
            <p>¡Gracias por elegirnos y que tenga un excelente estadía</p>
            <p>Hotel Bruno Relax and Flask</p>
            """
        print(f"correo enviado checkin a, {emailDestino}")
    else:
        msg = Message(
            subject="Bienvenido!",
            recipients=[emailDestino]
        )
        msg.html = f"""
            <p>Hola <strong>{nombre}</strong>,</p>
            <h2>¡Registro exitoso!</h2>
            <img src="cid:logo_email" width="200">
            <p>¡Gracias por ser parte de <b>la Estancia Bruno Relax and Flask</b>!</p>
            <p>Estamos felices de tenerte con nosotros 🤗</p>
        """

    msg.attach(
        filename="LOGO.png",
        content_type="image/png",
        data=imagenData,
        headers={"Content-ID": "<logo_email>"}
    )
    mail.send(msg)
    print("Backend: Se envió un email de bienvenida a:", emailDestino)

mail = Mail()

# la siguiente funcion solo admite un cursor ya inicializado
def obtenerHabitacionDisponible(tipo, fecha_entrada, fecha_salida, adultos, ninios, cursor):
    
    adultos = int(adultos or 0)
    ninios  = int(ninios or 0)

    capacidad_total = adultos + ninios

    cursor.execute("""
        SELECT id FROM habitaciones
        WHERE tipo = %s AND capacidad >= %s
    """, (tipo, capacidad_total))
    
    habitaciones = cursor.fetchall()

    if not habitaciones:
        return None

    for habitacion in habitaciones:
        habitacion_id = habitacion["id"]

        cursor.execute("""
            SELECT 1 FROM reservas
            WHERE habitacion_id = %s
            AND fecha_entrada < %s
            AND fecha_salida > %s
        """, (habitacion_id, fecha_salida, fecha_entrada))

        conflicto = cursor.fetchone()

        if not conflicto:
            return habitacion_id

    return None
