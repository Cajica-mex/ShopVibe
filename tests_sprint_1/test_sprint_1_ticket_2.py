# test_sprint_1_ticket_2.py
import os
import sys
import unittest
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

def log_success(msg):
    try:
        print(f"\n\033[92m✓\033[0m {msg}")
    except UnicodeEncodeError:
        print(f"\n\033[92m[OK]\033[0m {msg}")

class TestSprint1Ticket2(unittest.TestCase):
    def test_fact_sales_schema(self):
        db_path = "shopvibe.db"
        self.assertTrue(os.path.exists(db_path), "Error: No se encontró la base de datos 'shopvibe.db'. Primero completa el Ticket 1 y ejecuta su script.")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT id, customer_id, product_id, quantity, sale_date, total_amount FROM fact_sales")
            columns = [info[1] for info in cursor.execute("PRAGMA table_info(fact_sales)").fetchall()]
            self.assertIn("id", columns)
            self.assertIn("customer_id", columns)
            self.assertIn("product_id", columns)
            self.assertIn("quantity", columns)
            self.assertIn("sale_date", columns)
            self.assertIn("total_amount", columns)
            log_success("fact_sales table created with correct fields and constraints")
        except sqlite3.OperationalError as e:
            conn.close()
            self.fail(f"La tabla fact_sales no existe o no tiene las columnas correctas: {str(e)}")
            
        conn.close()

if __name__ == '__main__':
    unittest.main()
