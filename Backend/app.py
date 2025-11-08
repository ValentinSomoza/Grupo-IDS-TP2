from flask import Flask
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
import os

app = Flask(__name__)

def iniciarBaseDeDatos():
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
        )

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
    
@app.route("/")
def home():
    return "Flask se conecto a MariaDB correctamente !"

if __name__ == "__main__":
    app.run("127.0.0.1", port="5000", debug=True)

iniciarBaseDeDatos()