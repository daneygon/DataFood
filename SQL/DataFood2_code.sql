
USE master;
GO
IF DB_ID('DataFood2') IS NULL
    CREATE DATABASE DataFood2;
GO
USE DataFood2;
GO


-- ============================
-- 1) CREAR TABLAS

-- ============================
CREATE TABLE CategoriaInsumos (
    IDCategoriaInsumos INT PRIMARY KEY IDENTITY(1,1),
    NombreCategoria NVARCHAR(100)
);

CREATE TABLE Insumos (
    IDInsumos INT PRIMARY KEY IDENTITY(1,1),
    IDCategoriaInsumos INT NOT NULL REFERENCES CategoriaInsumos(IDCategoriaInsumos),
    NombreInsumo NVARCHAR(150),
    CantidadDisponible INT,
    CantidadDañada INT
);

CREATE TABLE TelefonoProveedores (
    IDTelefonoProveedores INT PRIMARY KEY IDENTITY(1,1),
    Telefono NVARCHAR(20)
);

CREATE TABLE Proveedores (
    IDProveedor INT PRIMARY KEY IDENTITY(1,1),
    NombreProveedor NVARCHAR(150),
    IDTelefonoProveedores INT NOT NULL REFERENCES TelefonoProveedores(IDTelefonoProveedores)
);


CREATE TABLE ProveedoresInsumos (
    IDProveedoresInsumos INT PRIMARY KEY IDENTITY(1,1),
    IDInsumos INT NULL,
    IDProveedor INT NOT NULL,
    PrecioCompra DECIMAL(10,2),
    CantidadComprada INT,
    Dia INT,
    Mes INT,
    Ano INT
);

-- Foreign Key hacia Insumos con SET NULL si se elimina un insumo
ALTER TABLE ProveedoresInsumos
ADD CONSTRAINT FK_ProveedoresInsumos_Insumos
FOREIGN KEY (IDInsumos)
REFERENCES Insumos(IDInsumos)
ON DELETE SET NULL;

-- Foreign Key hacia Proveedores (normal)
ALTER TABLE ProveedoresInsumos
ADD CONSTRAINT FK_ProveedoresInsumos_Proveedores
FOREIGN KEY (IDProveedor)
REFERENCES Proveedores(IDProveedor);


CREATE TABLE TelefonoCliente (
    IDTelefonoClientes INT PRIMARY KEY IDENTITY(1,1),
    Telefono NVARCHAR(20)
);

CREATE TABLE Clientes (
    IDClientes INT PRIMARY KEY IDENTITY(1,1),
    NumeroDeMesa INT,
    IDTelefonoClientes INT NOT NULL REFERENCES TelefonoCliente(IDTelefonoClientes),
    Nombre1 NVARCHAR(50),
    Nombre2 NVARCHAR(50) NULL,
    Apellido1 NVARCHAR(50),
    Apellido2 NVARCHAR(50) NULL
);

CREATE TABLE Produccion (
    IDProduccion INT PRIMARY KEY IDENTITY(1,1),
    CostoProduccionTotal DECIMAL(10,2),
    CostoPorPlato DECIMAL(10,2),
    CostoPorBebida DECIMAL(10,2),
    CantidadDeBebidas INT,
    CantidadDePlatos INT,
    NombreBebida NVARCHAR(100) NULL,
    NombrePlato NVARCHAR(100) NULL
);

CREATE TABLE CategoriaPlatos (
    IDCategoriaPlatos INT PRIMARY KEY IDENTITY(1,1),
    NombreCategoria NVARCHAR(100)
);

CREATE TABLE MenuDePlatos (
    IDMenuPlatos INT PRIMARY KEY IDENTITY(1,1),
    IDProduccion INT NOT NULL REFERENCES Produccion(IDProduccion),
    IDCategoriaPlatos INT NOT NULL REFERENCES CategoriaPlatos(IDCategoriaPlatos),
    NombrePlato NVARCHAR(150),
    Precio DECIMAL(10,2)
);

CREATE TABLE CategoriaBebidas (
    IDCategoriaBebidas INT PRIMARY KEY IDENTITY(1,1),
    NombreCategoria NVARCHAR(100)
);

CREATE TABLE MenuDeBebidas (
    IDMenuBebidas INT PRIMARY KEY IDENTITY(1,1),
    IDProduccion INT NOT NULL REFERENCES Produccion(IDProduccion),
    IDCategoriaBebidas INT NOT NULL REFERENCES CategoriaBebidas(IDCategoriaBebidas),
    NombreBebida NVARCHAR(150),
    Precio DECIMAL(10,2)
);

CREATE TABLE Venta (
    IDVentas INT PRIMARY KEY IDENTITY(1,1),
    MontoTotal DECIMAL(12,2) DEFAULT 0,
    Perdidas DECIMAL(12,2) DEFAULT 0,
    Ganancias DECIMAL(12,2) DEFAULT 0,
    Hora TIME DEFAULT CONVERT(TIME, GETDATE()),
    Dia INT DEFAULT DAY(GETDATE()),
    Mes INT DEFAULT MONTH(GETDATE()),
    Ano INT DEFAULT YEAR(GETDATE())
);

CREATE TABLE VentasClientesMenuBebidasMenuPlatos (
    IDVentasClientesMenuBebidasMenuPlatos INT PRIMARY KEY IDENTITY(1,1),
    IDVentas INT NOT NULL REFERENCES Venta(IDVentas),
    IDMenuBebidas INT NULL REFERENCES MenuDeBebidas(IDMenuBebidas),
    IDMenuPlatos INT NULL REFERENCES MenuDePlatos(IDMenuPlatos),
    IDClientes INT NULL REFERENCES Clientes(IDClientes),
    Cantidad INT NOT NULL,
    NombreBebida NVARCHAR(150) NULL,
    NombrePlato NVARCHAR(150) NULL,
    Precio DECIMAL(10,2) NOT NULL
);
GO

-- ============================
-- 2) INSERTAR 20 REGISTROS EN CADA TABLA
-- ============================

-- 2.1 Categorías de insumos (20)
INSERT INTO CategoriaInsumos (NombreCategoria) VALUES
('Lácteos'),('Carnes'),('Verduras'),('Frutas'),('Granos'),('Especias'),('Aceites'),('Bebidas'),('Panadería'),
('Azúcares'),('Conservas'),('Salsas'),('Congelados'),('Pescados'),('Legumbres'),('Hortalizas'),('Semillas'),
('Harinas'),('Líquidos y caldos'),('Otros');

-- 2.2 Insumos (20)
INSERT INTO Insumos (IDCategoriaInsumos, NombreInsumo, CantidadDisponible, CantidadDañada) VALUES
(1,'Queso seco (kg)',100,2),
(1,'Queso fresco (kg)',60,1),
(2,'Pollo entero (uds)',50,0),
(2,'Carne de res (kg)',40,0),
(3,'Tomate (kg)',120,3),
(3,'Cebolla (kg)',80,1),
(4,'Plátano verde (kg)',150,4),
(5,'Arroz (kg)',300,2),
(6,'Pimienta (kg)',10,0),
(7,'Aceite vegetal (L)',80,0),
(8,'Cacao en polvo (kg)',20,0),
(9,'Pan para desayuno (uds)',200,5),
(10,'Azúcar (kg)',100,1),
(11,'Jugo enlatado (uds)',60,0),
(12,'Salsa roja (L)',30,0),
(13,'Bolsa de hielo (kg)',50,0),
(14,'Filete pescado (kg)',25,0),
(15,'Frijoles rojos (kg)',90,5),
(16,'Zanahoria (kg)',70,2),
(17,'Semillas de achiote (kg)',5,0),
(18,'Harina de maíz (kg)',120,3),
(19,'Caldo de res (L)',20,0),
(20,'Servilletas (paquetes)',50,0);

-- 2.3 Teléfonos proveedores (20)
INSERT INTO TelefonoProveedores (Telefono) VALUES
('8888-0001'),('8888-0002'),('8955-1001'),('8955-1002'),('8887-2233'),
('8844-5566'),('8833-7788'),('8722-3344'),('8777-4455'),('8666-5544'),
('8555-6633'),('8444-7722'),('8333-8811'),('8222-9900'),('8111-0099'),
('8000-1111'),('7999-2222'),('7888-3333'),('7777-4444'),('7666-5555');

-- 2.4 Proveedores (20)
INSERT INTO Proveedores (NombreProveedor, IDTelefonoProveedores) VALUES
('Distribuidora La Finca',1),('Carnes del Norte',2),('Frutas y Verduras S.A.',3),('Panadería El Buen Pan',4),
('Bebidas Rápidas',5),('Abastecedora Central',6),('Mariscos del Pacífico',7),('Aromas y Especias',8),
('Aceites del Sur',9),('Cacao Oro',10),('Conservas Amigas',11),('Salsas y Más',12),('Hielo Express',13),
('Pescados y Más',14),('Legumbres La Tierra',15),('Hortalizas Unidas',16),('Semillas y Harinas',17),
('Harinas Modernas',18),('Caldos Selectos',19),('Suministros Útiles',20);

-- 2.5 ProveedoresInsumos (20)
INSERT INTO ProveedoresInsumos (IDInsumos, IDProveedor, PrecioCompra, CantidadComprada, Dia, Mes, Ano) VALUES
(1,1,1200.00,20,1,11,2025),
(2,1,900.00,15,2,11,2025),
(3,2,450.00,10,3,11,2025),
(4,2,1600.00,12,4,11,2025),
(5,3,300.00,40,5,11,2025),
(6,3,180.00,30,6,11,2025),
(7,4,250.00,60,7,11,2025),
(8,5,2400.00,100,8,11,2025),
(9,6,80.00,5,9,11,2025),
(10,7,600.00,20,10,11,2025),
(11,5,320.00,30,11,11,2025),
(12,12,200.00,10,12,11,2025),
(13,13,150.00,20,13,11,2025),
(14,14,800.00,8,14,11,2025),
(15,15,700.00,25,15,11,2025),
(16,16,140.00,30,16,11,2025),
(17,17,60.00,4,17,11,2025),
(18,18,360.00,40,18,11,2025),
(19,19,180.00,15,19,11,2025),
(20,20,120.00,10,20,11,2025);

-- 2.6 Teléfonos clientes (20)
INSERT INTO TelefonoCliente (Telefono) VALUES
('8855-1122'),('7844-2233'),('8881-3344'),('8882-4455'),('8883-5566'),
('8884-6677'),('8885-7788'),('8886-8899'),('8887-9900'),('8888-1010'),
('8889-1212'),('8890-1313'),('8891-1414'),('8892-1515'),('8893-1616'),
('8894-1717'),('8895-1818'),('8896-1919'),('8897-2020'),('8898-2121');

-- 2.7 Clientes (20) — incluyendo los 4 solicitados
INSERT INTO Clientes (NumeroDeMesa, IDTelefonoClientes, Nombre1, Nombre2, Apellido1, Apellido2) VALUES
(1,1,'Gamaliel','Joel','Gutierrez','Perez'),
(2,2,'Daney','Nohemi','Gonzalez','Marin'),
(3,3,'Marco','Aurelio','Lopez','Gonzalez'),
(4,4,'Maxwell','Antonio','Zeledon','Carballo'),
(5,5,'Ana',NULL,'Martinez','Lopez'),
(6,6,'Carlos',NULL,'Sanchez','Hernandez'),
(7,7,'Luisa','María','Diaz','Ramos'),
(8,8,'Pedro',NULL,'Alvarez','Mendoza'),
(9,9,'Lucia',NULL,'Ramirez','Ortiz'),
(10,10,'Rosa',NULL,'Gonzalez','Vega'),
(11,11,'Eduardo',NULL,'Cruz','Salinas'),
(12,12,'Fernanda',NULL,'Pinto','Ramos'),
(13,13,'Jorge',NULL,'Castro','Lopez'),
(14,14,'Marta',NULL,'Soto','Guzman'),
(15,15,'Diego',NULL,'Mejia','Paredes'),
(16,16,'Sonia',NULL,'Varela','Diaz'),
(17,17,'Ricardo',NULL,'Torres','Suarez'),
(18,18,'Patricia',NULL,'Molina','Navarro'),
(19,19,'Hector',NULL,'Silva','Ruiz'),
(20,20,'Beatriz',NULL,'Noguera','Cortes');



-- 1. Nacatamal
INSERT INTO Produccion (CostoPorPlato, CantidadDePlatos, NombrePlato)
VALUES (80.00, 15, 'Nacatamal');

-- 2. Indio Viejo
INSERT INTO Produccion (CostoPorPlato, CantidadDePlatos, NombrePlato)
VALUES (60.00, 20, 'Indio Viejo');

-- 3. Carne Guisada
INSERT INTO Produccion (CostoPorPlato, CantidadDePlatos, NombrePlato)
VALUES (90.00, 20, 'Carne Guisada');

-- 4. Gallo Pinto + Huevo
INSERT INTO Produccion (CostoPorPlato, CantidadDePlatos, NombrePlato)
VALUES (50.00, 12, 'Gallo Pinto + Huevo');

-- 5. Vigorón
INSERT INTO Produccion (CostoPorPlato, CantidadDePlatos, NombrePlato)
VALUES (45.00, 10, 'Vigorón');

-- 6. Pollo Asado
INSERT INTO Produccion (CostoPorPlato, CantidadDePlatos, NombrePlato)
VALUES (70.00, 14, 'Pollo Asado');

-- 7. Carne a la Plancha
INSERT INTO Produccion (CostoPorPlato, CantidadDePlatos, NombrePlato)
VALUES (65.00, 12, 'Carne a la Plancha');

-- 8. Sopa de Gallina
INSERT INTO Produccion (CostoPorPlato, CantidadDePlatos, NombrePlato)
VALUES (40.00, 10, 'Sopa de Gallina');

-- 9. Pescado Frito
INSERT INTO Produccion (CostoPorPlato, CantidadDePlatos, NombrePlato)
VALUES (55.00, 15, 'Pescado Frito');

-- 10. Bistec Encebollado
INSERT INTO Produccion (CostoPorPlato, CantidadDePlatos, NombrePlato)
VALUES (85.00, 18, 'Bistec Encebollado');

-- 12. Pollo al Horno
INSERT INTO Produccion (CostoPorPlato, CantidadDePlatos, NombrePlato)
VALUES (95.00, 16, 'Pollo al Horno');

-- 13. Ensalada Fresca
INSERT INTO Produccion (CostoPorPlato, CantidadDePlatos, NombrePlato)
VALUES (30.00, 6, 'Ensalada Fresca');

-- 14. Carne Asada
INSERT INTO Produccion (CostoPorPlato, CantidadDePlatos, NombrePlato)
VALUES (100.00, 20, 'Carne Asada');

-- 15. Plato Vegetariano
INSERT INTO Produccion (CostoPorPlato, CantidadDePlatos, NombrePlato)
VALUES (42.00, 9, 'Plato Vegetariano');

-- 16. Tajadas con Carne
INSERT INTO Produccion (CostoPorPlato, CantidadDePlatos, NombrePlato)
VALUES (48.00, 11, 'Tajadas con Carne');

-- 17. Camarones al Ajillo
INSERT INTO Produccion (CostoPorPlato, CantidadDePlatos, NombrePlato)
VALUES (68.00, 13, 'Camarones al Ajillo');

-- 18. Tamal de Elote
INSERT INTO Produccion (CostoPorPlato, CantidadDePlatos, NombrePlato)
VALUES (62.00, 12, 'Tamal de Elote');

-- 19. Quesillo con Tortillas
INSERT INTO Produccion (CostoPorPlato, CantidadDePlatos, NombrePlato)
VALUES (38.00, 8, 'Quesillo con Tortillas');

-- 20. Desayuno Ligero
INSERT INTO Produccion (CostoPorPlato, CantidadDePlatos, NombrePlato)
VALUES (34.00, 7, 'Desayuno Ligero');

-----------------bebida
-- 1. Fresco de Cacao
INSERT INTO Produccion (CostoPorBebida, CantidadDeBebidas, NombreBebida)
VALUES (25.00, 30, 'Fresco de Cacao');




-- 2.9 Categoría de platos (20)
INSERT INTO CategoriaPlatos (NombreCategoria) VALUES
('Desayunos'),('Entradas'),('Plato fuerte'),('Postres'),('Sopas'),('Mariscos'),('Vegetarianos'),
('Tradicionales'),('Combinados'),('A la plancha'),('Tortillas y panes'),('Ensaladas'),('Tacos'),
('Tajadas'),('Platos regionales'),('Rapidos'),('Guisados'),('Económicos'),('Especiales'),('Pescados');

-- 2.10 MenuDePlatos (20)
INSERT INTO MenuDePlatos (IDProduccion, IDCategoriaPlatos, NombrePlato, Precio) VALUES
(1,15,'Nacatamal',150.00),
(2,3,'Indio Viejo',140.00),
(3,17,'Carne Guisada',160.00),
(4,1,'Gallo Pinto + huevo',110.00),
(5,16,'Vigorón',130.00),
(6,3,'Pollo Asado',145.00),
(7,10,'Carne a la Plancha',155.00),
(8,5,'Sopa de Gallina',120.00),
(9,20,'Pescado Frito',170.00),
(10,3,'Bistec encebollado',165.00),
(11,5,'Sopa de Frijoles',100.00),
(12,3,'Pollo al horno',150.00),
(13,12,'Ensalada fresca',95.00),
(14,3,'Carne Asada',200.00),
(15,7,'Plato Vegetariano',120.00),
(16,9,'Tajadas con carne',135.00),
(17,6,'Camarones al ajillo',190.00),
(18,15,'Tamal de elote',110.00),
(19,11,'Quesillo con tortillas',85.00),
(20,1,'Desayuno ligero',90.00);

-- 2.11 Categoría de bebidas (20)
INSERT INTO CategoriaBebidas (NombreCategoria) VALUES
('Refrescos'),('Jugos naturales'),('Cafés'),('Tés'),('Aguas'),('Bebidas tradicionales'),('Calientes'),
('Frutales'),('Con leche'),('Sin azúcar'),('Enlatadas'),('Energéticas'),('Batidos'),('Yogurt'),
('Licuados'),('Nacionales'),('Especiales'),('Digestivas'),('Alcoholicas (no venta)'),('Otras');

-- 2.12 MenuDeBebidas (20)
INSERT INTO MenuDeBebidas (IDProduccion, IDCategoriaBebidas, NombreBebida, Precio) VALUES
(1,8,'Fresco de Cacao',45.00),
(2,6,'Chicha de Maíz',40.00),
(3,3,'Café con Pan',35.00),
(4,1,'Fresco de Tamarindo',38.00),
(5,2,'Jugo de Mango',42.00),
(6,1,'Fresco de Piña',40.00),
(7,11,'Refresco (gaseosa 500ml)',30.00),
(8,2,'Jugo de Guayaba',36.00),
(9,1,'Fresco de Cebada',32.00),
(10,4,'Limonada con hierbabuena',28.00),
(11,4,'Té frío',25.00),
(12,2,'Jugo de Papaya',44.00),
(13,5,'Agua de coco',30.00),
(14,7,'Chocolate Caliente',50.00),
(15,2,'Fresco de Maracuyá',43.00),
(16,2,'Jugo de Nance',39.00),
(17,2,'Chicha de Piña',41.00),
(18,8,'Fresco de Guineo',34.00),
(19,1,'Refresco Natural',27.00),
(20,3,'Café Negro',22.00);

