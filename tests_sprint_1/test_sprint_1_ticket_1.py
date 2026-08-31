# test_sprint_1_ticket_1.py
import os
import sys
import unittest
import sqlite3
import subprocess

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

def log_success(msg):
    try:
        print(f"\n\033[92m✓\033[0m {msg}")
    except UnicodeEncodeError:
        print(f"\n\033[92m[OK]\033[0m {msg}")

class TestSprint1Ticket1(unittest.TestCase):
    
    def setUp(self):
        self.db_path = "shopvibe.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def tearDown(self):
        # We leave the database intact for manual inspections by the student,
        # but clean it up if needed.
        pass

    def test_database_ingestion_pipeline(self):
        # 1. Verify schema creation via create_tables.py
        script_create = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/create_tables.py'))
        try:
            subprocess.run([sys.executable, script_create], check=True, capture_output=True, text=True)
            log_success("src/create_tables.py ejecutado correctamente sin errores.")
        except subprocess.CalledProcessError as e:
            self.fail(f"El script src/create_tables.py falló: {e.stderr}")
            
        self.assertTrue(os.path.exists(self.db_path), "Error: No se creó la base de datos 'shopvibe.db'.")
        
        # 2. Check if SQLite tables were created
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Verify dim_customers schema
        try:
            cursor.execute("SELECT id, customer_name, email FROM dim_customers")
            log_success("Tabla dim_customers creada en SQLite con el esquema correcto.")
        except sqlite3.OperationalError as e:
            conn.close()
            self.fail(f"Error en la tabla dim_customers: {str(e)}")
            
        # Verify dim_products schema
        try:
            cursor.execute("SELECT id, product_name, price, category FROM dim_products")
            log_success("Tabla dim_products creada en SQLite con el esquema correcto.")
        except sqlite3.OperationalError as e:
            conn.close()
            self.fail(f"Error en la tabla dim_products: {str(e)}")
            
        # Verify fact_sales schema
        try:
            cursor.execute("SELECT id, customer_id, product_id, quantity, sale_date, total_amount FROM fact_sales")
            log_success("Tabla fact_sales creada en SQLite con el esquema correcto.")
        except sqlite3.OperationalError as e:
            conn.close()
            self.fail(f"Error en la tabla fact_sales: {str(e)}")
            
        conn.close()

        # 3. Verify data backfill ingestion via backfill_job.py
        script_backfill = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/backfill_job.py'))
        try:
            subprocess.run([sys.executable, script_backfill], check=True, capture_output=True, text=True)
            log_success("src/backfill_job.py ejecutado correctamente sin errores.")
        except subprocess.CalledProcessError as e:
            self.fail(f"El script src/backfill_job.py falló: {e.stderr}")
            
        # 4. Check loaded records
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # dim_products should contain 5 products
        cursor.execute("SELECT COUNT(*) FROM dim_products")
        prod_count = cursor.fetchone()[0]
        self.assertEqual(prod_count, 5, f"Esperaba 5 productos en dim_products, se encontraron {prod_count}.")
        log_success("dim_products poblada correctamente (5 productos).")
        
        # dim_customers should contain unique customers (4 customers in generator logs)
        cursor.execute("SELECT COUNT(*) FROM dim_customers")
        cust_count = cursor.fetchone()[0]
        self.assertGreater(cust_count, 0, "No se insertaron clientes en dim_customers.")
        log_success(f"dim_customers poblada correctamente ({cust_count} clientes únicos).")
        
        # fact_sales should contain sales (20 orders in generator logs)
        cursor.execute("SELECT COUNT(*) FROM fact_sales")
        sales_count = cursor.fetchone()[0]
        self.assertEqual(sales_count, 20, f"Esperaba 20 ventas en fact_sales, se encontraron {sales_count}.")
        log_success("fact_sales poblada correctamente (20 registros de ventas).")
        
        conn.close()

if __name__ == '__main__':
    unittest.main()
