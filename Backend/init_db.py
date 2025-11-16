from db import get_conection

with open("Backend/init_db.sql") as f:
    sql = f.read()

conn = get_conection()
cursor = conn.cursor()
for statement in sql.split(";"):
    if statement.strip():
        print(statement)
        cursor.execute(statement)
        conn.commit()
        print("Sentencia ejecutada")
cursor.close()
conn.close()