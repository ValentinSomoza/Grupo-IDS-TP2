CREATE DATABASE IF NOT EXISTS HotelFAF;
USE HotelFAF;

CREATE TABLE IF NOT EXISTS habitaciones (
    id VARCHAR(10) PRIMARY KEY,
    numero INT(3), 
    precio FLOAT(6,2),
    estado BOOLEAN,
    capacidad INT(2),
    descripcion VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    email VARCHAR(50),
    documento INT(7),
    fecha_registro DATE,
    telefono INT(15)
);

CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    noches INT,
    ninios INT,
    adultos INT,
    id_habitacion VARCHAR(10),
    fecha_entrada DATE,
    fecha_salida DATE,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id) ON DELETE CASCADE,
    FOREIGN KEY (id_habitacion) REFERENCES habitaciones(id) ON DELETE CASCADE
);

