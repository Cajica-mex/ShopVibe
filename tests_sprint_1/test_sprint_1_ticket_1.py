# test_sprint_1_ticket_1.py
import os
import sys
import unittest
import sqlite3
import subprocess

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class TestSprint1Ticket1(unittest.TestCase):
    
    def test_database_creation_and_schema(self):
        db_path = "shopvibe.db"
        if os.path.exists(db_path):
            os.remove(db_path)
            
        # Run create_tables.py script
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/create_tables.py'))
        try:
            result = subprocess.run([sys.executable, script_path], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            self.fail(f"El script src/create_tables.py falló al ejecutarse: {e.stderr}")
            
        # Verify database file exists
        self.assertTrue(os.path.exists(db_path), "Error: No se creó el archivo de base de datos 'shopvibe.db'.")
        
        # Verify tables and columns
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verify dim_products table
        try:
            cursor.execute("SELECT id, product_name, price, category FROM dim_products")
            columns = [info[1] for info in cursor.execute("PRAGMA table_info(dim_products)").fetchall()]
            self.assertIn("id", columns, "Falta la columna 'id' en dim_products")
            self.assertIn("product_name", columns, "Falta la columna 'product_name' en dim_products")
            self.assertIn("price", columns, "Falta la columna 'price' en dim_products")
            self.assertIn("category", columns, "Falta la columna 'category' en dim_products")
        except sqlite3.OperationalError as e:
            conn.close()
            self.fail(f"La tabla dim_products no existe o no tiene las columnas correctas: {str(e)}")
            
        # Verify dim_customers table
        try:
            cursor.execute("SELECT id, customer_name, email FROM dim_customers")
            columns = [info[1] for info in cursor.execute("PRAGMA table_info(dim_customers)").fetchall()]
            self.assertIn("id", columns, "Falta la columna 'id' en dim_customers")
            self.assertIn("customer_name", columns, "Falta la columna 'customer_name' en dim_customers")
            self.assertIn("email", columns, "Falta la columna 'email' en dim_customers")
        except sqlite3.OperationalError as e:
            conn.close()
            self.fail(f"La tabla dim_customers no existe o no tiene las columnas correctas: {str(e)}")
            
        conn.close()

if __name__ == '__main__':
    unittest.main()
