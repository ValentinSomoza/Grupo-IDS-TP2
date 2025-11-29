CREATE DATABASE IF NOT EXISTS HotelBruno;
USE HotelBruno;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    nombreUsuario VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(50),
    dniPasaporte VARCHAR(50),
    contrasenia VARCHAR(255),
    fechaCreacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fechaActualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS habitaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero INT UNIQUE NOT NULL,
    tipo ENUM(
        'simple',
        'doble',
        'matrimonial',
        'ejecutivo',
        'familiar',
        'deluxe',
        'panoramica',
        'presidencial'
    ) NOT NULL,
    capacidad INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,

    nombre VARCHAR(50),
    apellido VARCHAR(50),
    email VARCHAR(100),
    telefono VARCHAR(20),
    documento VARCHAR(20),

    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ninios INT,
    adultos INT,
    fecha_entrada DATE,
    fecha_salida DATE,
    habitacion_id INT NOT NULL,
    checkin BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (habitacion_id) REFERENCES habitaciones(id)
);

CREATE TABLE IF NOT EXISTS imagenes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    nombre VARCHAR(100),
    ruta VARCHAR(255) NOT NULL,
    orden INT NOT NULL
);
 
CREATE TABLE IF NOT EXISTS textos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    orden INT NOT NULL DEFAULT 0
);

INSERT INTO habitaciones (numero, tipo, capacidad, precio)
VALUES
(101, 'simple',       1, 100000.00),
(102, 'simple',       1, 100000.00),
(201, 'doble',        2, 200000.00),
(202, 'doble',        2, 200000.00),
(301, 'matrimonial',  2, 300000.00),
(302, 'matrimonial',  2, 300000.00),
(401, 'ejecutivo',    4, 400000.00),
(402, 'ejecutivo',    4, 400000.00),
(501, 'familiar',     5, 500000.00),
(502, 'familiar',     5, 500000.00),
(601, 'deluxe',       6, 600000.00),
(602, 'deluxe',       6, 600000.00),
(701, 'panoramica',   7, 700000.00),
(702, 'panoramica',   7, 700000.00),
(801, 'presidencial', 8, 800000.00),
(802, 'presidencial', 8, 800000.00);