-- ============================================================
-- FerreSys - Esquema de Base de Datos
-- ============================================================
DROP DATABASE IF EXISTS ferresys_db;

CREATE DATABASE ferresys_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE ferresys_db;

-- ------------------------------------------------------------
-- Tabla: categorias
-- ------------------------------------------------------------
CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(150)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Tabla: productos
-- ------------------------------------------------------------
CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    codigo_barras VARCHAR(30) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    precio_compra DECIMAL(10,2) NOT NULL CHECK (precio_compra >= 0),
    precio_venta DECIMAL(10,2) NOT NULL CHECK (precio_venta >= 0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    stock_minimo INT NOT NULL DEFAULT 5 CHECK (stock_minimo >= 0),
    id_categoria INT,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Tabla: clientes
-- ------------------------------------------------------------
CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion VARCHAR(150)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Tabla: ventas
-- ------------------------------------------------------------
CREATE TABLE ventas (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    fecha_venta DATETIME DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    id_cliente INT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Tabla: detalle_ventas
-- ------------------------------------------------------------
CREATE TABLE detalle_ventas (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Datos de ejemplo (opcionales)
-- ------------------------------------------------------------
INSERT INTO categorias (nombre, descripcion) VALUES
('Herramientas manuales', 'Martillos, destornilladores, alicates, etc.'),
('Eléctricos', 'Taladros, sierras, pulidoras'),
('Plomería', 'Tuberías, llaves, codos'),
('Pinturas', 'Pinturas, brochas, rodillos');

INSERT INTO productos (codigo_barras, nombre, precio_compra, precio_venta, stock, stock_minimo, id_categoria) VALUES
('7501000000011', 'Martillo de acero 16oz', 45000, 75000, 20, 5, 1),
('7501000000028', 'Juego destornilladores x6', 32000, 58000, 15, 5, 1),
('7501000000035', 'Taladro percutor 650W', 180000, 289000, 8, 3, 2),
('7501000000042', 'Cinta teflón 1/2"', 1500, 3000, 100, 20, 3),
('7501000000059', 'Pintura blanca 1 galón', 45000, 78000, 12, 4, 4);

INSERT INTO clientes (nombre, telefono, email, direccion) VALUES
('Cliente Genérico', '000-000-0000', 'generico@ferresys.local', 'N/A');
