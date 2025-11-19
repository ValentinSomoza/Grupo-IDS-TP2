CREATE DATABASE IF NOT EXISTS HotelBruno;
USE HotelBruno;

CREATE TABLE IF NOT EXISTS habitaciones (
    id VARCHAR(10) PRIMARY KEY,
    numero INT(3), 
    precio FLOAT(6,2),
    estado BOOLEAN,
    capacidad INT(2),
    descripcion VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    email VARCHAR(50),
    documento VARCHAR(20),
    fecha_registro DATE,
    telefono VARCHAR(20),
    noches INT,
    ninios INT,
    adultos INT,
    fecha_entrada DATE,
    fecha_salida DATE,
    id_habitacion VARCHAR(10),
    checkin BOOLEAN
);

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