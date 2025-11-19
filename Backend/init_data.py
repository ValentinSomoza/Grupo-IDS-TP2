from db import obtener_conexion_con_el_servidor

def crearUsuarioTest():
    conexion = obtener_conexion_con_el_servidor()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE nombreUsuario = %s", ("pepe",))
    existe = cursor.fetchone()

    if not existe:
        cursor.execute("""
            INSERT INTO usuarios (nombre, apellido, nombreUsuario, email, telefono, dniPasaporte, contrasenia)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, ("pepe", "mujica", "pepe", "aplicarmt@gmail.com", "01234567890", "01234567890", "mujica"))
        conexion.commit()
        print("Backend: Usuario legendario PEPE creado automáticamente.")

    cursor.close()
    conexion.close()