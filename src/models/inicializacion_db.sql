-- #############################################
-- # Archivo: src\models\inicializacion_db.sql #
-- #############################################

-- Crear la tabla 'roles' para definir los permisos de los usuarios
CREATE TABLE IF NOT EXISTS roles (
    id_rol SERIAL PRIMARY KEY,
    nombre_rol VARCHAR(50) UNIQUE NOT NULL
);

-- Insertar datos iniciales en la tabla 'roles'
INSERT INTO roles (nombre_rol)
VALUES 
    ('admin'),
    ('artista'),
    ('cliente')
ON CONFLICT (nombre_rol) DO NOTHING;

-- Crear la tabla 'usuarios' con referencia a 'roles'
CREATE TABLE IF NOT EXISTS usuarios (
    email VARCHAR(255) PRIMARY KEY,
    nombre_usuario VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    id_rol INT REFERENCES roles(id_rol) DEFAULT 3  -- Rol de cliente por defecto
);

-- Insertar datos iniciales en la tabla 'usuarios'
INSERT INTO usuarios (email, nombre_usuario, password, id_rol)
VALUES 
    ('admin@example.com', 'admin', 'adminpass', 1),
    ('artista1@example.com', 'artista1', 'artistapass1', 2),
    ('cliente1@example.com', 'cliente1', 'clientepass1', 3)
ON CONFLICT (email) DO NOTHING;

-- Crear la tabla 'generos' para clasificar canciones o álbumes
CREATE TABLE IF NOT EXISTS generos (
    id_genero SERIAL PRIMARY KEY,
    nombre_genero VARCHAR(255) NOT NULL UNIQUE
);

-- Insertar datos de ejemplo en la tabla 'generos'
INSERT INTO generos (nombre_genero)
VALUES 
    ('Rock'),
    ('Pop'),
    ('Jazz'),
    ('Hip-Hop')
ON CONFLICT (nombre_genero) DO NOTHING;

-- Crear la tabla 'canciones' para almacenar información sobre canciones
CREATE TABLE IF NOT EXISTS canciones (
    codigo VARCHAR(10) PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    artista VARCHAR(255) NOT NULL,
    album VARCHAR(255),
    duracion TIME NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    ventas INT NOT NULL DEFAULT 0,
    id_genero INT REFERENCES generos(id_genero),
    fecha_lanzamiento DATE DEFAULT CURRENT_DATE
);

-- Insertar datos de ejemplo en la tabla 'canciones'
INSERT INTO canciones (codigo, titulo, artista, album, duracion, precio, ventas, id_genero, fecha_lanzamiento)
VALUES 
    ('001', 'Bohemian Rhapsody', 'Queen', 'A Night at the Opera', '00:05:55', 1.99, 5000, 1, '1975-10-31'),
    ('002', 'Hotel California', 'Eagles', 'Hotel California', '00:06:30', 1.99, 4000, 1, '1976-12-08'),
    ('003', 'Thriller', 'Michael Jackson', 'Thriller', '00:05:57', 1.99, 10000, 2, '1982-11-30'),
    ('004', 'Like a Prayer', 'Madonna', 'Like a Prayer', '00:05:41', 1.99, 3000, 2, '1989-03-03'),
    ('005', 'Take Five', 'Dave Brubeck', 'Time Out', '00:05:24', 1.99, 2000, 3, '1959-07-01'),
    ('006', 'What a Wonderful World', 'Louis Armstrong', NULL, '00:02:21', 1.99, 3500, 3, '1967-09-01'),
    ('007', 'Lose Yourself', 'Eminem', '8 Mile', '00:05:26', 1.99, 8000, 4, '2002-10-22'),
    ('008', 'Juicy', 'The Notorious B.I.G.', 'Ready to Die', '00:05:02', 1.99, 5000, 4, '1994-08-08')
ON CONFLICT (codigo) DO NOTHING;

-- Crear la tabla 'ventas' para registrar ventas individuales
CREATE TABLE IF NOT EXISTS ventas (
    id_venta SERIAL PRIMARY KEY,
    id_cancion VARCHAR(10) REFERENCES canciones(codigo),
    email_usuario VARCHAR(255) REFERENCES usuarios(email),
    cantidad_vendida INT NOT NULL,
    fecha_venta DATE DEFAULT CURRENT_DATE
);

-- Insertar datos de ejemplo en la tabla 'ventas'
INSERT INTO ventas (id_cancion, email_usuario, cantidad_vendida, fecha_venta)
VALUES 
    ('001', 'cliente1@example.com', 2, '2024-11-13'),
    ('003', 'cliente1@example.com', 1, '2024-11-14'),
    ('004', 'artista1@example.com', 1, '2024-11-15'),
    ('007', 'cliente1@example.com', 3, '2024-11-15'),
    ('008', 'cliente1@example.com', 4, '2024-11-16'),
    ('005', 'cliente1@example.com', 1, '2024-11-17'),
    ('002', 'cliente1@example.com', 2, '2024-11-18')
ON CONFLICT DO NOTHING;

-- #############################################
-- Consultas de verificación de datos
-- #############################################

-- Consultar todas las ventas con detalles de usuario y canción
SELECT v.id_venta, u.email AS usuario, c.titulo AS cancion, v.cantidad_vendida, v.fecha_venta
FROM ventas v
JOIN usuarios u ON v.email_usuario = u.email
JOIN canciones c ON v.id_cancion = c.codigo;

-- Consultar el total de ventas por canción
SELECT titulo, artista, ventas, precio 
FROM canciones;
