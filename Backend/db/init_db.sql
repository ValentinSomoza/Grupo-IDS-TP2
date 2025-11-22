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
    tipo ENUM('simple', 'doble', 'matrimonial', 'king', 'suite') NOT NULL,
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
    noches INT,
    ninios INT,
    adultos INT,
    fecha_entrada DATE,
    fecha_salida DATE,
    habitacion_id INT NOT NULL,
    checkin BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (habitacion_id) REFERENCES habitaciones(id)
);

CREATE TABLE IF NOT EXISTS checkin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    email VARCHAR(100),
    dniPasaporte VARCHAR(20),
    telefono VARCHAR(20),
    tipoHabitacionC VARCHAR(10),
    numeroHabitacionC VARCHAR(20), 
    fechaEntradaC DATE,
    fechaSalidaC DATE,
    reserva_id VARCHAR(10)
);

INSERT INTO habitaciones (numero, tipo, capacidad, precio)
VALUES
(101, 'simple', 1, 10.00),
(102, 'simple', 1, 10.00),
(201, 'doble', 2, 20.00),
(202, 'doble', 2, 20.00),
(301, 'matrimonial', 2, 30.00),
(302, 'matrimonial', 2, 30.00),
(401, 'suite', 4, 40.00),
(402, 'suite', 4, 40.00),
(501, 'king', 3, 50.00),
(502, 'king', 3, 50.00);