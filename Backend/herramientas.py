from flask_mail import Mail, Message
from email.mime.image import MIMEImage
import os

def enviarMail(emailDestino, nombre):
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

    rutaLogo = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "Frontend", "static", "images", "LOGO.png")
    )

    with open(rutaLogo, "rb") as img:
        imagenData = img.read()

    msg.attach(
        filename="LOGO.png",
        content_type="image/png",
        data=imagenData,
        headers={"Content-ID": "<logo_email>"}
    )

    mail.send(msg)
    print("Backend: Se envió un email de bienvenida a:", emailDestino)

mail = Mail()