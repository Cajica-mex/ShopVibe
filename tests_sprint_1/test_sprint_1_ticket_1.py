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
            
        self.create_tables_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/create_tables.py'))
        self.backfill_job_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/backfill_job.py'))

    def test_scratch_files_conventions(self):
        # 1. Verify files exist
        self.assertTrue(os.path.exists(self.create_tables_path), "Error: No se encontró el archivo 'src/create_tables.py'. Debes crearlo desde cero.")
        self.assertTrue(os.path.exists(self.backfill_job_path), "Error: No se encontró el archivo 'src/backfill_job.py'. Debes crearlo desde cero.")
        log_success("Archivos src/create_tables.py y src/backfill_job.py creados desde cero.")

        # 2. Inspect src/create_tables.py content
        with open(self.create_tables_path, "r", encoding="utf-8") as f:
            create_code = f.read()
            
        self.assertIn("close(", create_code, "Error en src/create_tables.py: Recuerda llamar a .close() para cerrar la conexión a la base de datos.")
        self.assertTrue(
            'if __name__ == "__main__":' in create_code or "if __name__ == '__main__':" in create_code,
            "Error en src/create_tables.py: Recuerda estructurar la ejecución del script con if __name__ == '__main__':"
        )
        self.assertTrue(
            'db_path = "shopvibe.db"' in create_code or "db_path = 'shopvibe.db'" in create_code,
            "Error en src/create_tables.py: Define db_path = 'shopvibe.db'"
        )
        self.assertTrue(
            'schema_path = "schema.sql"' in create_code or "schema_path = 'schema.sql'" in create_code,
            "Error en src/create_tables.py: Define schema_path = 'schema.sql'"
        )
        log_success("src/create_tables.py cumple con todas las variables locales, cierre de conexiones y bloque main estándar.")

        # 3. Inspect src/backfill_job.py content
        with open(self.backfill_job_path, "r", encoding="utf-8") as f:
            backfill_code = f.read()
            
        self.assertIn("close(", backfill_code, "Error en src/backfill_job.py: Recuerda llamar a .close() para cerrar la conexión a la base de datos.")
        self.assertTrue(
            'if __name__ == "__main__":' in backfill_code or "if __name__ == '__main__':" in backfill_code,
            "Error en src/backfill_job.py: Recuerda estructurar la ejecución del script con if __name__ == '__main__':"
        )
        self.assertIn("def run_backfill(", backfill_code, "Error en src/backfill_job.py: Define la función run_backfill() en el script.")
        log_success("src/backfill_job.py cumple con la función run_backfill(), cierre de conexiones y bloque main estándar.")

    def test_database_ingestion_pipeline(self):
        # We need this to ensure the files exist before running subprocess
        if not os.path.exists(self.create_tables_path) or not os.path.exists(self.backfill_job_path):
            self.skipTest("Ignorando pipeline de base de datos debido a que los archivos del código no existen todavía.")

        # 1. Run create_tables.py
        try:
            subprocess.run([sys.executable, self.create_tables_path], check=True, capture_output=True, text=True)
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

        # 3. Run backfill_job.py
        try:
            subprocess.run([sys.executable, self.backfill_job_path], check=True, capture_output=True, text=True)
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
