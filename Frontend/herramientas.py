from flask import request, session
import requests
import os

from static.data.nombresYcomentarios import habitaciones, servicios, resenias, index_textos

def estaLogeado():
    nombreUsuario = request.args.get("nombreUsuario") or session.get("nombreUsuario")
    if not nombreUsuario:
        return None
    return nombreUsuario

def enviarImagenesAlBackend():
    rutaBase = os.path.join(os.path.dirname(__file__), "static", "images")
    rutaBase = os.path.abspath(rutaBase)

    extensiones = (".jpg", ".jpeg", ".png", ".webp")
    rutas = []

    ignorarCarpeta = "basicos"

    for raiz, directorios, archivos in os.walk(rutaBase):

        directorios[:] = [directorio for directorio in directorios if directorio != ignorarCarpeta]

        for archivo in archivos:

            nombreArchivo = archivo.lower()

            if nombreArchivo == "logo.png":
                continue

            if nombreArchivo.endswith(extensiones):

                rutaCompleta = os.path.join(raiz, archivo).replace("\\", "/")

                rutaRelativa = os.path.relpath(rutaCompleta, rutaBase).replace("\\", "/")

                rutas.append(f"static/images/{rutaRelativa}")

    try:
        respuesta = requests.post(
            f"{os.getenv('BACKEND_URL')}/datosIndex/cargar-imagenes",
            json={"imagenes": rutas},
            timeout=3
        )
        return respuesta.json()

    except Exception as e:
        return {"error": f"No se pudo enviar imágenes desde el front: {str(e)}"}

def enviarComentariosYNombresBackend():
    url = f"{os.getenv('BACKEND_URL')}/datosIndex/cargar-textos"

    datosTextos = {
        "habitaciones": habitaciones,
        "servicios": servicios,
        "resenias": resenias,
        "index": index_textos
    }

    try:
        respuesta = requests.post(url, json=datosTextos, timeout=3)
        return respuesta.json()
    except Exception as e:
        return {"error": f"No se pudo enviar textos desde el front: {str(e)}"}