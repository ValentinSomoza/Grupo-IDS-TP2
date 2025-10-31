from flask import Flask, render_template, url_for

app = Flask(__name__)

if __name__ == "__main__":
    app.run("127.0.0.1", port="8080", debug=True)