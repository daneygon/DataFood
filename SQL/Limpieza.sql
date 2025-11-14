USE DataFood2;
GO

DECLARE @sql NVARCHAR(MAX) = N'';

SELECT @sql += 'DROP TRIGGER [' + s.name + '].[' + t.name + '];'
FROM sys.triggers t
JOIN sys.objects o ON t.parent_id = o.object_id
JOIN sys.schemas s ON o.schema_id = s.schema_id;

PRINT @sql;
EXEC sp_executesql @sql;

USE DataFood2;
GO

ALTER TABLE Produccion
DROP COLUMN CostoProduccionTotal;

ALTER TABLE Produccion
ADD CostoProduccionTotal DECIMAL(10,2) NULL;

SELECT *
FROM Produccion
