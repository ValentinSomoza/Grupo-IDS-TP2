from flask import Flask, request, jsonify
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
import os
from flask_mail import Mail, Message

app = Flask(__name__)

load_dotenv()
def conectarBaseDatos():
    try: 
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS")
        )
    except Error as e:
        print("Error al conectar con la base de datos ", e)
        return None
    
def iniciarBaseDeDatos():
    try:
        conexion = conectarBaseDatos()

        if conexion.is_connected():
            cursor = conexion.cursor()

            sql_path = os.path.join(os.path.dirname(__file__), "db", "init_db.sql")

            with open(sql_path, "r") as f:
                sql_script = f.read()
            
            for statement in sql_script.split(";"):
                stmt = statement.strip()
                if stmt:
                    cursor.execute(stmt)
            
            conexion.commit()
            print("Base de datos inicializada !")
    
    except Error as e:
        print("Base de datos no pudo inicializarse debido al error ", e)
    
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

def create_app():

    app = Flask(__name__)

    reservas = []

    @app.route("/")
    def home():
        return "Flask se conectó a MariaDB correctamente!"

    iniciarBaseDeDatos()

    @app.route("/reservas", methods=["POST"])
    def recibirReserva():
        data = request.get_json()
        reservas.append(data)
        print("Nueva reserva: ", data)

        return jsonify({"mensaje": "Reserva guardada con exito !"}), 200
    return app

@app.route('/clientes', methods=['GET'])
def clientes():
    conexion = conectarBaseDatos()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("USE HotelFAF")
    cursor.execute("SELECT * FROM clientes")
    listaClientes = cursor.fetchall()
    conexion.close()
    return jsonify(listaClientes),200

@app.route('/cliente/<id>', methods=['GET'])
def cliente(id):
    conexion = conectarBaseDatos()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("USE HotelFAF")
    cursor.execute(
        "SELECT nombre, apellido, email,fecha_registro, documento, telefono FROM clientes WHERE id = %s",(id,))
    listaClientes = cursor.fetchall()
    conexion.close()
    return jsonify(listaClientes),200

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

@app.route("/checkinFormulario", methods=["POST"])
def checkinFormulario():
    if request.method == "POST":
        print("checkin ejeucattddooooo")
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        documento = request.form.get("dniPasaporte")
        tipoHabitacion = request.form.get("tipo-habitacion")
        fechaEntrada = request.form.get("fecha-entrada")
        fechaSalida = request.form.get("fecha-salida")
        emailUsuario = request.form.get("email")
        telefono = request.form.get("telefono")

        print(f"El backend recibió un nuevo checkin:\n Nombre:{nombre}\n,Apellido:{apellido}") 

        emailEstancia = "estanciabruno@gmail.com"

        mensaje = request.form.get("mensaje")

        msg = Message(
            "Check-in Estancia Bruno",
            recipients=[emailUsuario, emailEstancia])
        msg.body = (
            f"Estimado {nombre},\n"
            f"Gracias por preferirnos, Estos son los detalles del checkin\n"
            f"DATOS DEL TITULAR:\n"
            f"Nombre: {nombre}, {apellido}\n"
            f"Documento: {documento}\n"
            f"Email: {emailUsuario}\n" 
            f"Teléfono: {telefono}\n" 
            f"ESTADIA:\n"
            f"Habitacion: {tipoHabitacion}\n"
            f"Fecha de entrada: {fechaEntrada}\n"
            f"Fecha de salida: {fechaSalida}\n"
        )
        try:
            mail.send(msg)
            return jsonify({"ok": True, "msg": "Check-in registrado y correo enviado"})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
