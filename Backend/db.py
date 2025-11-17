import mysql.connector

def get_conection():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "admin",
        database = "HotelFAF"
    )