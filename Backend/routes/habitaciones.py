from flask import Blueprint, jsonify, request

habitaciones_bp = Blueprint("Habitaciones", __name__)

@habitaciones_bp.route("/")
def get_clientes():
    pass