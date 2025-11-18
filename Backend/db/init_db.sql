DROP DATABASE IF EXISTS HotelFAF;
CREATE DATABASE HotelFAF;
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
    id_habitacion VARCHAR(10),
    fecha_entrada DATE,
    fecha_salida DATE,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id) ON DELETE CASCADE,
    FOREIGN KEY (id_habitacion) REFERENCES habitaciones(id) ON DELETE CASCADE
    
);

INSERT INTO clientes (nombre, apellido, email, documento, fecha_registro, telefono) VALUES
('Ronny', 'Mamani', 'rm@gmail.com', 123456, '2023-01-15', 9876543),
('Maria', 'Garcia', 'mg@gmailcom', 654321, '2023-02-20', 912345),
('Pedro', 'Lopez', 'pl@gmial.com', 112233, '2023-03-10', 998877);

INSERT INTO habitaciones (id, numero, precio, estado, capacidad, descripcion) VALUES
('H001', 101, 150.00, TRUE, 2, 'Habitacion doble con vista al mar'),
('H002', 102, 200.00, TRUE, 4, 'Suite familiar con balcon'),
('H003', 103, 100.00, FALSE, 1, 'Habitacion individual');

INSERT INTO reservas (id_cliente, id_habitacion, fecha_entrada, fecha_salida) VALUES
(1, 'H001', '2023-05-01', '2023-05-05'),
(2, 'H002', '2023-06-10', '2023-06-15'),
(3, 'H003', '2023-07-20', '2023-07-22');


/*
INSERT INTO reservas (nombre, apellido, email, documento, fecha_registro, telefono, noches, ninios, adultos,id_habitacion, fecha_entrada, fecha_salida) VALUES
('Manolo','Perez','ManoloPerez@Gatorade.com',12123123,'2002-12-3',123456,3,4,1, 'H001', '2023-05-01', '2023-05-05');
*/


/*
    FOREIGN KEY (id_habitacion) REFERENCES habitaciones(id) ON DELETE CASCADE
*/