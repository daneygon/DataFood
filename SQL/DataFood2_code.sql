
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

----ARREGLO PARA IMAGENES------------------
USE DataFood2;
GO

ALTER TABLE Produccion
ADD Imagen VARBINARY(MAX) NULL;
GO

ALTER TABLE Produccion
ADD ImagenContentType NVARCHAR(50) NULL;
GO
------------------------------------------ARREGLO


---MODIFICAR QUE TENGA FECHA Y DIA 
USE DataFood2;
GO

-- 1. Agregar columnas de fecha a Produccion
ALTER TABLE Produccion 
ADD Dia INT NULL,
    Mes INT NULL,
    Ano INT NULL;
GO

-- 2. Agregar valores por defecto (hoy) para nuevas filas
ALTER TABLE Produccion 
ADD CONSTRAINT DF_Produccion_Dia DEFAULT (DAY(GETDATE())) FOR Dia;
GO

ALTER TABLE Produccion 
ADD CONSTRAINT DF_Produccion_Mes DEFAULT (MONTH(GETDATE())) FOR Mes;
GO

ALTER TABLE Produccion 
ADD CONSTRAINT DF_Produccion_Ano DEFAULT (YEAR(GETDATE())) FOR Ano;
GO

-- 3. Rellenar los registros que ya existían sin fecha
UPDATE Produccion
SET Dia = ISNULL(Dia, DAY(GETDATE())),
    Mes = ISNULL(Mes, MONTH(GETDATE())),
    Ano = ISNULL(Ano, YEAR(GETDATE()));
GO


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

