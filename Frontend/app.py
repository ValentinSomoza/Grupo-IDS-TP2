from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from herramientas import estaLogeado, enviarImagenesAlBackend, enviarComentariosYNombresBackend
import json
import requests
from datetime import date
import base64
import os
from datetime import datetime
from routes.checkin import checkin_bp
from routes.cuenta import cuenta_bp
from routes.ingreso import ingreso_bp
from routes.reservas import reservas_bp
from routes.registro import registro_bp
from routes.autenticacion import autenticacion_bp
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")

resultadoImagenes = enviarImagenesAlBackend()
mensajeImagenes = resultadoImagenes.get("mensaje") or resultadoImagenes.get("error")
print("Frontend: Se enviaron las imagenes al backend y la respuesta fue: ", mensajeImagenes)

resultadoTextos = enviarComentariosYNombresBackend()
mensajeTextos = resultadoTextos.get("mensaje") or resultadoTextos.get("error")
numeroNombres = resultadoTextos.get("total_nombres")
numeroComentarios = resultadoTextos.get("total_comentarios")
print("Frontend: Se enviaron los textos al backend y la respuesta fue: ", mensajeTextos, " \n Cantidad de nombres cargados: ", numeroNombres, " \n Cantidad de comentarios cargados: ", numeroComentarios)

app.register_blueprint(checkin_bp, url_prefix="/checkin")
app.register_blueprint(cuenta_bp, url_prefix="/cuenta")
app.register_blueprint(ingreso_bp, url_prefix="/ingreso")
app.register_blueprint(reservas_bp, url_prefix="/reservas")
app.register_blueprint(registro_bp, url_prefix="/registro")
app.register_blueprint(autenticacion_bp, url_prefix="/autenticacion")

@app.route("/")
def index():
    backendUrl = os.getenv("BACKEND_URL")
    return render_template("index.html", backend_url=backendUrl)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/galeria")
def galeria():
    return render_template("galeria.html", backend_url=os.getenv("BACKEND_URL"))

@app.route("/mapa")
def mapa():
    return render_template('mapa.html')

@app.route("/contacto")
def contacto():
    return render_template('contacto.html')

@app.route("/eligeDatos")
def eligeDatos():
    if estaLogeado() is None:
        flash("⚠️ Debes iniciar sesión antes de hacer una reserva", "warning")
        return redirect(url_for('ingreso.ingreso'))
    return render_template("eligeDatos.html")