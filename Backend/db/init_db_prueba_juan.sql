CREATE DATABASE IF NOT EXISTS HotelFAF_Test;
USE HotelFAF_Test;

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