from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('Erro404.html'), 404

@app.route("/galeria")
def galeria():
    return render_template('galeria.html')

if __name__ == "__main__":
    app.run("127.0.0.1", port="5001", debug=True)