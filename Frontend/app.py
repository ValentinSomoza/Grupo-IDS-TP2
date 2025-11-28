from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from herramientas import estaLogeado
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

def create_app():

    app = Flask(__name__)
    app.secret_key = os.getenv("APP_SECRET_KEY")

    app.register_blueprint(checkin_bp, url_prefix="/checkin")
    app.register_blueprint(cuenta_bp, url_prefix="/cuenta")
    app.register_blueprint(ingreso_bp, url_prefix="/ingreso")
    app.register_blueprint(reservas_bp, url_prefix="/reservas")
    app.register_blueprint(registro_bp, url_prefix="/registro")
    app.register_blueprint(autenticacion_bp, url_prefix="/autenticacion")

    @app.route("/")
    def index():
        return render_template('index.html', backend_url=os.getenv("BACKEND_URL"))

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

    return app
