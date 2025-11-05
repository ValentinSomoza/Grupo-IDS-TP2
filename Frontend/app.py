from flask import Flask, render_template, request
app = Flask(__name__)

# Ruta principal
@app.route("/")
def home():
    return render_template("index.html")

# Ruta para la página de reservas
@app.route("/reserva")
def reserva():
    return render_template("reserva.html")

# Nueva ruta para procesar el formulario
@app.route("/procesar_reserva", methods=["POST"])
def procesar_reserva():
    # Aquí recibes los datos del formulario
    nombre = request.form.get("nombre_huesped")
    apellido = request.form.get("apellido_huesped")
    email = request.form.get("email_huesped")

    # Podría guardarlos en una base de datos o hacer algo con ellos
    # Por ahora devolvemos un mensaje simple
    return f"Reserva confirmada para {nombre} {apellido}. Confirmación enviada a {email}"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)