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
    
    def test_database_creation_and_schema(self):
        db_path = "shopvibe.db"
        if os.path.exists(db_path):
            os.remove(db_path)
            
        # Run create_tables.py script
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/create_tables.py'))
        try:
            result = subprocess.run([sys.executable, script_path], check=True, capture_output=True, text=True)
            log_success("src/create_tables.py executed successfully without errors")
        except subprocess.CalledProcessError as e:
            self.fail(f"El script src/create_tables.py falló al ejecutarse: {e.stderr}")
            
        # Verify database file exists
        self.assertTrue(os.path.exists(db_path))
        log_success("Database file shopvibe.db created successfully")
        
        # Verify tables and columns
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verify dim_products table
        try:
            cursor.execute("SELECT id, product_name, price, category FROM dim_products")
            columns = [info[1] for info in cursor.execute("PRAGMA table_info(dim_products)").fetchall()]
            self.assertIn("id", columns)
            self.assertIn("product_name", columns)
            self.assertIn("price", columns)
            self.assertIn("category", columns)
            log_success("dim_products table created with correct fields and constraints")
        except sqlite3.OperationalError as e:
            conn.close()
            self.fail(f"La tabla dim_products no existe o no tiene las columnas correctas: {str(e)}")
            
        # Verify dim_customers table
        try:
            cursor.execute("SELECT id, customer_name, email FROM dim_customers")
            columns = [info[1] for info in cursor.execute("PRAGMA table_info(dim_customers)").fetchall()]
            self.assertIn("id", columns)
            self.assertIn("customer_name", columns)
            self.assertIn("email", columns)
            log_success("dim_customers table created with correct fields and constraints")
        except sqlite3.OperationalError as e:
            conn.close()
            self.fail(f"La tabla dim_customers no existe o no tiene las columnas correctas: {str(e)}")
            
        conn.close()

if __name__ == '__main__':
    unittest.main()
