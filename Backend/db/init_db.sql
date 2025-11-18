DROP DATABASE IF EXISTS HotelFAF;
CREATE DATABASE HotelFAF;
USE HotelFAF;

CREATE TABLE IF NOT EXISTS usuarios (
    id VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    nombreUsuario VARCHAR(50),
    email VARCHAR(50),
    telefono INT(15),
    documento INT(10),
    contraseña VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS habitaciones (
    id VARCHAR(10) PRIMARY KEY,
    numero INT(3), 
    precio FLOAT(6,2),
    estado BOOLEAN,
    capacidad INT(2),
    descripcion VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS reservas (
    id VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(50),
    documento INT(10),
    apellido VARCHAR(50),
    nombreUsuario VARCHAR(50),
    email VARCHAR(50),
    telefono INT(15),
    fechaEntrada DATE,
    fechaSalida DATE,
    adultos INT(1),
    niños INT(1),
    tipoHabitacion VARCHAR(20),
    numeroHabitacion VARCHAR(20),
    costo INT(12)
);

CREATE TABLE IF NOT EXISTS checkin (
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    email VARCHAR(50),
    documento INT(7),
    telefono INT(15),
    tipoHabitacionC VARCHAR(10),
    numeroHabitacionC VARCHAR(20), 
    fechaEntradaC DATE,
    fechaSalidaC DATE,

    FOREIGN KEY (tipoHabitacionC) REFERENCES habitaciones(id),
    FOREIGN KEY (numeroHabitacionC) REFERENCES reservas(numeroHabitacion),
    FOREIGN KEY (fechaEntradaC) REFERENCES reservas(fechaEntrada),
    FOREIGN KEY (fechaSalidaC) REFERENCES reservas(fechaEntrada),

);

/*
INSERT INTO reservas (nombre, apellido, email, documento, fecha_registro, telefono, noches, ninios, adultos,id_habitacion, fecha_entrada, fecha_salida) VALUES
('Manolo','Perez','ManoloPerez@Gatorade.com',12123123,'2002-12-3',123456,3,4,1, 'H001', '2023-05-01', '2023-05-05');
*/


/*
    FOREIGN KEY (id_habitacion) REFERENCES habitaciones(id) ON DELETE CASCADE
*/