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

CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    email VARCHAR(50),
    documento INT(7),
    fecha_registro DATE,
    telefono INT,
    noches INT,
    ninios INT,
    adultos INT,
    fecha_entrada DATE,
    fecha_salida DATE,
    id_habitacion VARCHAR(10),
    FOREIGN KEY (id_habitacion) REFERENCES habitaciones(id) ON DELETE CASCADE
);


INSERT INTO reservas (nombre, apellido, email, documento, fecha_registro, telefono, noches, ninios, adultos,id_habitacion, fecha_entrada, fecha_salida) VALUES
('Manolo','Perez','ManoloPerez@Gatorade.com',12123123,'2002-12-3',123456,3,4,1, 'H001', '2023-05-01', '2023-05-05');
