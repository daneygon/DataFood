import pyodbc # type: ignore

def conectar():
    try:
        conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=LAPTOP-H4V75VLP;'
            'DATABASE=DataFood2;'
            'Trusted_Connection=yes;'
        )
        print(" Conexión establecida con SQL Server (DataFood2)")
        return conexion
    except Exception as e:
        print(" Error al conectar:", e)
        return None
