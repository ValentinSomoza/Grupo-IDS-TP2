from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/")
def reserva():
    return render_template("reserva.html")

@app.route("/procesar_reserva", methods=["POST"])
def procesar_reserva():

    nombre = request.form.get("nombre_huesped")
    apellido = request.form.get("apellido_huesped")
    email = request.form.get("email_huesped")

    return f"Reserva confirmada para {nombre} {apellido}. Confirmación enviada a {email}"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)