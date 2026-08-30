# create_tables.py
import sqlite3
import os

def crear_tablas():
    db_path = "shopvibe.db"
    schema_path = "schema.sql"
    
    if not os.path.exists(schema_path):
        print(f"Error: No se encontró el archivo {schema_path}")
        return
        
    print(f"Leyendo esquema de {schema_path}...")
    with open(schema_path, "r", encoding="utf-8") as f:
        sql_script = f.read()
        
    print(f"Conectando a SQLite ({db_path}) y ejecutando DDL...")
    # TODO: Conectar a la base de datos 'shopvibe.db'
    # Ejecutar el script SQL del archivo schema.sql en la base de datos
    # Hacer commit y cerrar la conexión
    pass

if __name__ == "__main__":
    crear_tablas()
