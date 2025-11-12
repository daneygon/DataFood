
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
    IDInsumos INT NOT NULL REFERENCES Insumos(IDInsumos),
    IDProveedor INT NOT NULL REFERENCES Proveedores(IDProveedor),
    PrecioCompra DECIMAL(10,2),
    CantidadComprada INT,
    Dia INT,
    Mes INT,
    Ano INT
);

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

-- 2.8 Producción (20)
USE DataFood2;
GO


-- 2. Crea una nueva columna calculada automáticamente


ALTER TABLE Produccion
DROP COLUMN CostoProduccionTotal;

ALTER TABLE Produccion
ADD CostoProduccionTotal AS (
    CASE
        WHEN CantidadDePlatos IS NOT NULL AND CostoPorPlato IS NOT NULL
            THEN CostoPorPlato * CantidadDePlatos
        WHEN CantidadDeBebidas IS NOT NULL AND CostoPorBebida IS NOT NULL
            THEN CostoPorBebida * CantidadDeBebidas
        ELSE 0
    END
);


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

-- 2.13 No se crean ventas vacías: con opción A el detalle crea ventas automáticamente.
-- (Si quieres ventas vacías también, puedo agregarlas, pero no es necesario.)

GO

-- ============================
-- 3) TRIGGER: INSTEAD OF INSERT en detalle -> Crear Venta + insertar detalle
-- ============================
CREATE TRIGGER trg_Detail_INSTEADOF_Insert_CreateVenta
ON VentasClientesMenuBebidasMenuPlatos
INSTEAD OF INSERT
AS
BEGIN
    SET NOCOUNT ON;

    -- Guardamos los datos a procesar en una tabla temporal/variable
    DECLARE @tmp TABLE (
        RowID INT IDENTITY(1,1) PRIMARY KEY,
        IDMenuBebidas INT NULL,
        IDMenuPlatos INT NULL,
        IDClientes INT NULL,
        Cantidad INT,
        NombreBebida NVARCHAR(150) NULL,
        NombrePlato NVARCHAR(150) NULL,
        Precio DECIMAL(10,2)
    );

    INSERT INTO @tmp (IDMenuBebidas, IDMenuPlatos, IDClientes, Cantidad, NombreBebida, NombrePlato, Precio)
    SELECT IDMenuBebidas, IDMenuPlatos, IDClientes, Cantidad, NombreBebida, NombrePlato, Precio
    FROM inserted;

    DECLARE @maxRow INT = (SELECT MAX(RowID) FROM @tmp);
    DECLARE @current INT = 1;

    WHILE @current IS NOT NULL AND @current <= ISNULL(@maxRow,0)
    BEGIN
        DECLARE @idMenuB INT = (SELECT IDMenuBebidas FROM @tmp WHERE RowID = @current);
        DECLARE @idMenuP INT = (SELECT IDMenuPlatos FROM @tmp WHERE RowID = @current);
        DECLARE @idCliente INT = (SELECT IDClientes FROM @tmp WHERE RowID = @current);
        DECLARE @cantidad INT = (SELECT Cantidad FROM @tmp WHERE RowID = @current);
        DECLARE @nombreB NVARCHAR(150) = (SELECT NombreBebida FROM @tmp WHERE RowID = @current);
        DECLARE @nombreP NVARCHAR(150) = (SELECT NombrePlato FROM @tmp WHERE RowID = @current);
        DECLARE @precio DECIMAL(10,2) = (SELECT Precio FROM @tmp WHERE RowID = @current);

        -- 1) Crear la venta (se usan valores por defecto para Hora/Dia/Mes/Ano)
        INSERT INTO Venta DEFAULT VALUES;
        DECLARE @newVentaID INT = SCOPE_IDENTITY();

        -- 2) Calcular MontoTotal y CostoTotal según si es plato o bebida
        DECLARE @montoTotal DECIMAL(12,2) = ISNULL(@precio,0) * ISNULL(@cantidad,0);
        DECLARE @costoUnit DECIMAL(12,2) = 0;
        DECLARE @costoTotal DECIMAL(12,2) = 0;

        IF @idMenuP IS NOT NULL
        BEGIN
            SELECT @costoUnit = p.CostoPorPlato
            FROM MenuDePlatos mp
            INNER JOIN Produccion p ON mp.IDProduccion = p.IDProduccion
            WHERE mp.IDMenuPlatos = @idMenuP;
        END
        ELSE IF @idMenuB IS NOT NULL
        BEGIN
            SELECT @costoUnit = p.CostoPorBebida
            FROM MenuDeBebidas mb
            INNER JOIN Produccion p ON mb.IDProduccion = p.IDProduccion
            WHERE mb.IDMenuBebidas = @idMenuB;
        END

        SET @costoTotal = ISNULL(@costoUnit,0) * ISNULL(@cantidad,0);

        DECLARE @ganancia DECIMAL(12,2) = 0;
        DECLARE @perdida DECIMAL(12,2) = 0;

        IF @montoTotal >= @costoTotal
        BEGIN
            SET @ganancia = @montoTotal - @costoTotal;
            SET @perdida = 0;
        END
        ELSE
        BEGIN
            SET @ganancia = 0;
            SET @perdida = @costoTotal - @montoTotal;
        END

        -- 3) Actualizar la venta con los totales calculados
        UPDATE Venta
        SET MontoTotal = @montoTotal,
            Ganancias = @ganancia,
            Perdidas = @perdida,
            Hora = CONVERT(TIME, GETDATE()),
            Dia = DAY(GETDATE()),
            Mes = MONTH(GETDATE()),
            Ano = YEAR(GETDATE())
        WHERE IDVentas = @newVentaID;

        -- 4) Insertar el detalle asignándole el IDVentas creado
        INSERT INTO VentasClientesMenuBebidasMenuPlatos (IDVentas, IDMenuBebidas, IDMenuPlatos, IDClientes, Cantidad, NombreBebida, NombrePlato, Precio)
        VALUES (@newVentaID, @idMenuB, @idMenuP, @idCliente, @cantidad, @nombreB, @nombreP, @precio);

        SET @current = @current + 1;
    END
END;
GO

-- ============================
-- 4) TRIGGERS AFTER UPDATE y AFTER DELETE -> recalculan totales para ventas afectadas
-- ============================
CREATE TRIGGER trg_Recalc_AFTER_Update
ON VentasClientesMenuBebidasMenuPlatos
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    ;WITH VentasAfectadas AS (
        SELECT DISTINCT IDVentas FROM inserted
        UNION
        SELECT DISTINCT IDVentas FROM deleted
    )
    UPDATE v
    SET 
        MontoTotal = ISNULL(t.TotalMonto,0),
        Ganancias = CASE 
                        WHEN ISNULL(t.TotalMonto,0) >= ISNULL(t.TotalCosto,0) THEN ISNULL(t.TotalMonto - t.TotalCosto,0)
                        ELSE 0
                    END,
        Perdidas = CASE 
                        WHEN ISNULL(t.TotalMonto,0) < ISNULL(t.TotalCosto,0) THEN ISNULL(t.TotalCosto - t.TotalMonto,0)
                        ELSE 0
                  END
    FROM Venta v
    INNER JOIN VentasAfectadas va ON v.IDVentas = va.IDVentas
    LEFT JOIN (
        SELECT
            d.IDVentas,
            SUM(d.Cantidad * d.Precio) AS TotalMonto,
            SUM(
                CASE 
                    WHEN d.IDMenuPlatos IS NOT NULL THEN ISNULL(p.CostoPorPlato,0) * d.Cantidad
                    WHEN d.IDMenuBebidas IS NOT NULL THEN ISNULL(p2.CostoPorBebida,0) * d.Cantidad
                    ELSE 0
                END
            ) AS TotalCosto
        FROM VentasClientesMenuBebidasMenuPlatos d
        LEFT JOIN MenuDePlatos mp ON d.IDMenuPlatos = mp.IDMenuPlatos
        LEFT JOIN Produccion p ON mp.IDProduccion = p.IDProduccion
        LEFT JOIN MenuDeBebidas mb ON d.IDMenuBebidas = mb.IDMenuBebidas
        LEFT JOIN Produccion p2 ON mb.IDProduccion = p2.IDProduccion
        GROUP BY d.IDVentas
    ) t ON t.IDVentas = v.IDVentas;
END;
GO

CREATE TRIGGER trg_Recalc_AFTER_Delete
ON VentasClientesMenuBebidasMenuPlatos
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;

    ;WITH VentasAfectadas AS (
        SELECT DISTINCT IDVentas FROM deleted
    )
    UPDATE v
    SET 
        MontoTotal = ISNULL(t.TotalMonto,0),
        Ganancias = CASE 
                        WHEN ISNULL(t.TotalMonto,0) >= ISNULL(t.TotalCosto,0) THEN ISNULL(t.TotalMonto - t.TotalCosto,0)
                        ELSE 0
                    END,
        Perdidas = CASE 
                        WHEN ISNULL(t.TotalMonto,0) < ISNULL(t.TotalCosto,0) THEN ISNULL(t.TotalCosto - t.TotalMonto,0)
                        ELSE 0
                  END
    FROM Venta v
    INNER JOIN VentasAfectadas va ON v.IDVentas = va.IDVentas
    LEFT JOIN (
        SELECT
            d.IDVentas,
            SUM(d.Cantidad * d.Precio) AS TotalMonto,
            SUM(
                CASE 
                    WHEN d.IDMenuPlatos IS NOT NULL THEN ISNULL(p.CostoPorPlato,0) * d.Cantidad
                    WHEN d.IDMenuBebidas IS NOT NULL THEN ISNULL(p2.CostoPorBebida,0) * d.Cantidad
                    ELSE 0
                END
            ) AS TotalCosto
        FROM VentasClientesMenuBebidasMenuPlatos d
        LEFT JOIN MenuDePlatos mp ON d.IDMenuPlatos = mp.IDMenuPlatos
        LEFT JOIN Produccion p ON mp.IDProduccion = p.IDProduccion
        LEFT JOIN MenuDeBebidas mb ON d.IDMenuBebidas = mb.IDMenuBebidas
        LEFT JOIN Produccion p2 ON mb.IDProduccion = p2.IDProduccion
        GROUP BY d.IDVentas
    ) t ON t.IDVentas = v.IDVentas;
END;
GO



-- ============================
-- 5) EJEMPLOS: Insertar algunos detalles (al hacer esto se crean ventas automáticamente)
-- ============================
-- Ejemplo 1: Insertar un detalle (solo plato). Esto creará una fila en Venta + detalle.
INSERT INTO VentasClientesMenuBebidasMenuPlatos (IDMenuBebidas, IDMenuPlatos, IDClientes, Cantidad, NombreBebida, NombrePlato, Precio)
VALUES (NULL, 1, 1, 2, NULL, 'Nacatamal', 150.00);

-- Ejemplo 2: Insertar un detalle (plato + bebida en un solo registro, se considerará como un item con precio aplicado)
INSERT INTO VentasClientesMenuBebidasMenuPlatos (IDMenuBebidas, IDMenuPlatos, IDClientes, Cantidad, NombreBebida, NombrePlato, Precio)
VALUES (1, 6, 3, 1, 'Fresco de Cacao', 'Pollo Asado', 165.00);

-- Ejemplo 3: Bebida sola
INSERT INTO VentasClientesMenuBebidasMenuPlatos (IDMenuBebidas, IDMenuPlatos, IDClientes, Cantidad, NombreBebida, NombrePlato, Precio)
VALUES (2, NULL, 2, 1, 'Chicha de Maíz', NULL, 40.00);

-- Venta solo plato
INSERT INTO VentasClientesMenuBebidasMenuPlatos (IDMenuBebidas, IDMenuPlatos, IDClientes, Cantidad, NombreBebida, NombrePlato, Precio)
VALUES (NULL, 3, 4, 1, NULL, 'Carne Guisada', 160.00);

-- Venta solo bebida
INSERT INTO VentasClientesMenuBebidasMenuPlatos (IDMenuBebidas, IDMenuPlatos, IDClientes, Cantidad, NombreBebida, NombrePlato, Precio)
VALUES (4, NULL, 5, 2, 'Fresco de Tamarindo', NULL, 38.00);

-- Venta plato + bebida
INSERT INTO VentasClientesMenuBebidasMenuPlatos (IDMenuBebidas, IDMenuPlatos, IDClientes, Cantidad, NombreBebida, NombrePlato, Precio)
VALUES (3, 7, 6, 1, 'Café con Pan', 'Carne a la Plancha', 185.00);

-- Venta múltiple para un cliente
INSERT INTO VentasClientesMenuBebidasMenuPlatos (IDMenuBebidas, IDMenuPlatos, IDClientes, Cantidad, NombreBebida, NombrePlato, Precio)
VALUES 
(NULL, 12, 7, 2, NULL, 'Pollo al horno', 150.00),
(12, NULL, 7, 1, 'Jugo de Papaya', NULL, 44.00);

-- (Puedes insertar más detalles; cada INSERT generará su propia Venta asociada.)

GO
-- FIN DEL SCRIPT
