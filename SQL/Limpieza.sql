USE DataFood2;
GO

-- ==========================================
-- 🔻 1️⃣ DESACTIVAR RESTRICCIONES TEMPORALMENTE
-- ==========================================
ALTER TABLE VentasClientesMenuBebidasMenuPlatos NOCHECK CONSTRAINT ALL;
ALTER TABLE MenuDePlatos NOCHECK CONSTRAINT ALL;
ALTER TABLE MenuDeBebidas NOCHECK CONSTRAINT ALL;
ALTER TABLE Produccion NOCHECK CONSTRAINT ALL;

-- ==========================================
-- 🧹 2️⃣ ELIMINAR DATOS EN ORDEN SEGURO (HIJOS → PADRES)
-- ==========================================
DELETE FROM VentasClientesMenuBebidasMenuPlatos;
DELETE FROM MenuDePlatos;
DELETE FROM MenuDeBebidas;
DELETE FROM Produccion;

-- ==========================================
-- 🔄 3️⃣ REINICIAR CONTADORES IDENTITY
-- ==========================================
DBCC CHECKIDENT ('VentasClientesMenuBebidasMenuPlatos', RESEED, 0);
DBCC CHECKIDENT ('MenuDePlatos', RESEED, 0);
DBCC CHECKIDENT ('MenuDeBebidas', RESEED, 0);
DBCC CHECKIDENT ('Produccion', RESEED, 0);

-- ==========================================
-- 🔒 4️⃣ REACTIVAR LAS RESTRICCIONES DE FOREIGN KEYS
-- ==========================================
ALTER TABLE Produccion CHECK CONSTRAINT ALL;
ALTER TABLE MenuDeBebidas CHECK CONSTRAINT ALL;
ALTER TABLE MenuDePlatos CHECK CONSTRAINT ALL;
ALTER TABLE VentasClientesMenuBebidasMenuPlatos CHECK CONSTRAINT ALL;

-- ==========================================
-- ✅ 5️⃣ VERIFICAR RESULTADO FINAL
-- ==========================================
SELECT 
    'Produccion' AS Tabla, COUNT(*) AS Registros FROM Produccion
UNION ALL
SELECT 
    'MenuDeBebidas', COUNT(*) FROM MenuDeBebidas
UNION ALL
SELECT 
    'MenuDePlatos', COUNT(*) FROM MenuDePlatos
UNION ALL
SELECT 
    'VentasClientesMenuBebidasMenuPlatos', COUNT(*) FROM VentasClientesMenuBebidasMenuPlatos;
GO

-- ==========================================
-- 🧾 6️⃣ CONFIRMAR SECUENCIA ACTUAL (OPCIONAL)
-- ==========================================
DBCC CHECKIDENT ('Produccion');
DBCC CHECKIDENT ('MenuDePlatos');
DBCC CHECKIDENT ('MenuDeBebidas');
DBCC CHECKIDENT ('VentasClientesMenuBebidasMenuPlatos');
GO

DELETE FROM Venta
WHERE IDVentas NOT IN (SELECT DISTINCT IDVentas FROM VentasClientesMenuBebidasMenuPlatos);

UPDATE Produccion
SET CostoPorPlato = ISNULL(CostoPorPlato, 0),
    CostoPorBebida = ISNULL(CostoPorBebida, 0);
