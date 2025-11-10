from flask import Flask
from flask_cors import CORS
from Backend.routes.clientes import clientes_bp
from Backend.routes.habitaciones import habitaciones_bp
from Backend.routes.reservas import reservas_bp

app = Flask(__name__)
CORS(app)
#No estoy seguro de que esos prefix sean correctos, cualquier cosa despues los cambiamos
app.register_blueprint(clientes_bp, url_prefix="/clientes")
app.register_blueprint(habitaciones_bp, url_prefix="/habitaciones")
app.register_blueprint(reservas_bp, url_prefix="/reservas")

if __name__ == "__main__":
    app.run("127.0.0.1", port="5001", debug=True)