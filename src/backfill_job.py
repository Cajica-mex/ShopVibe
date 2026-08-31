# backfill_job.py
import os
import csv
import json
import sqlite3

def run_backfill():
    db_path = "shopvibe.db"
    products_csv = "data/raw/products.csv"
    orders_json = "data/raw/sales_orders.json"
    
    if not os.path.exists(db_path):
        print(f"Error: No se encontró la base de datos '{db_path}'. Asegúrate de ejecutar create_tables.py primero.")
        return

    print("Iniciando proceso de backfill de datos...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # --- TODO: Tu código aquí ---
    # 1. Leer data/raw/products.csv e insertar productos en dim_products
    # 2. Leer data/raw/sales_orders.json, extraer clientes únicos e insertar en dim_customers
    # 3. Extraer e insertar las órdenes de venta en fact_sales
    # ----------------------------
    
    conn.commit()
    conn.close()
    print("Backfill de datos completado.")

if __name__ == "__main__":
    run_backfill()
