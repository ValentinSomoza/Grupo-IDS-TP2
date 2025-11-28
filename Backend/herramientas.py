from flask_mail import Mail, Message
from email.mime.image import MIMEImage
from db import obtener_conexion_con_el_servidor
import os

def enviarMail(emailDestino, nombre, esCheckin):
    
    rutaLogo = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "Frontend", "static", "images", "LOGO.png")
    )

    try:
        with open("../Frontend/static/images/LOGO.png", "rb") as img:
            imagenData = img.read()

            if not imagenData:
                imagenData = None
    except:
        print("Ocurrio un error al cargar el logo, pero no imposibilitamos la salida del mail")
        imagenData = None

    if isinstance(esCheckin, dict):
        
        msg = Message(
            subject="Chenck-in Hotel Bruno!",
            recipients=[emailDestino]
        )
        msg.html = f"""
            <p>Hola <strong>{nombre}</strong>,</p>

            <h2>¡Tu check-in ha sido registrado con éxito!</h2>

            <p>Nos alegra confirmarte que tu reserva ya está activa. A continuación encontrarás los detalles de tu registro:</p>

            <ul>
                <li><strong>Nombre completo:</strong> {esCheckin['nombre']} {esCheckin['apellido']}</li>
                <li><strong>DNI / Pasaporte:</strong> {esCheckin['documento']}</li>
                <li><strong>Fecha de entrada:</strong> {esCheckin['fecha_entrada']}</li>
                <li><strong>Fecha de salida:</strong> {esCheckin['fecha_salida']}</li>
                <li><strong>ID de la reserva:</strong> {esCheckin['id']}</li>
                <li><strong>ID de habitación:</strong> {esCheckin['habitacion_id']}</li>
            </ul>

            <p>Esperamos que disfrutes de tu estadía con nosotros. Si tenés alguna consulta adicional, no dudes en responder a este correo o comunicarte con nuestra recepción.</p>

            <img src="cid:logo_email" width="200" alt="Logo Hotel Bruno">

            <p>¡Gracias por elegirnos!</p>
            <p><em>Hotel Bruno Relax and Flask</em></p>
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

    if imagenData != None:
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

def cargarImagenesBD(app):

    carpetaBase = os.path.join(app.static_folder, "images")
    extensiones = (".jpg", ".jpeg", ".png", ".webp")

    cantidadTotal = 0

    conn = obtener_conexion_con_el_servidor()
    cursor = conn.cursor()

    for carpeta in os.listdir(carpetaBase):
        rutaCarpeta = os.path.join(carpetaBase, carpeta)
        if not os.path.isdir(rutaCarpeta):
            continue

        tipoImagen = carpeta.lower()

        archivos = sorted(os.listdir(rutaCarpeta))
        orden = 1

        for archivo in archivos:
            if archivo.lower().endswith(extensiones):
                rutaRelativa = f"/static/images/{carpeta}/{archivo}"

                cursor.execute("SELECT id FROM imagenes WHERE ruta=%s", (rutaRelativa,))
                existe = cursor.fetchone()

                if not existe:
                    cursor.execute(
                        "INSERT INTO imagenes (tipo, nombre, ruta, orden) VALUES (%s, %s, %s, %s)",
                        (tipoImagen, archivo, rutaRelativa, orden)
                    )
                    cantidadTotal += 1
                    orden += 1

    conn.commit()
    cursor.close()
    conn.close()

    return cantidadTotal