from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

API_BASE = "http://localhost:5001"

#esta funcion no estoy seguro de que si va bien aca, pero cualquier cosa la movemos al backend
def agregar_usuario(nombre,apellido, email, usuario, contrasenia):
    response = request.get(f"{API_BASE}/usuario/{usuario}",json={"nombre":nombre,"apellido":apellido,"email":email,"contrasenia":contrasenia})
    return response.status_code == 201
#⬆Esto estoy casi seguro que esta mal, pero lo voy a corregir⬆


@app.route("/")
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/galeria")
def galeria():
    return render_template('galeria.html')

@app.route("/mapa")
def mapa():
    return render_template('mapa.html')

if __name__ == "__main__":
    app.run("127.0.0.1", port="5001", debug=True)