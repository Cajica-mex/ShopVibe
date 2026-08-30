# test_sprint_1_ticket_13.py
import os
import sys
import unittest
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class TestSprint1Ticket13(unittest.TestCase):
    def test_unique_ingestion_control(self):
        try:
            from db_loader import insertar_con_control
        except ImportError:
            self.fail("No se pudo importar insertar_con_control")
            
        db_path = "test_loader_t13.db"
        if os.path.exists(db_path):
            os.remove(db_path)
            
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE fact_sales (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                sale_date TEXT,
                total_amount REAL
            )
        """)
        conn.commit()
        
        test_records = [
            {"id": 201, "customer_id": 1, "product_id": 2, "quantity": 1, "fecha": "2026-08-20", "monto": 10.0},
            {"id": 202, "customer_id": 2, "product_id": 3, "quantity": 2, "fecha": "2026-08-20", "monto": 30.0}
        ]
        
        for r in test_records:
            insertar_con_control(conn, r)
            
        cursor.execute("SELECT COUNT(*) FROM fact_sales")
        self.assertEqual(cursor.fetchone()[0], 2)
        
        # Test unique control
        dup_record = {"id": 201, "customer_id": 1, "product_id": 2, "quantity": 1, "fecha": "2026-08-20", "monto": 10.0}
        insertar_con_control(conn, dup_record)
        cursor.execute("SELECT COUNT(*) FROM fact_sales")
        self.assertEqual(cursor.fetchone()[0], 2)
        
        conn.close()
        if os.path.exists(db_path):
            os.remove(db_path)

if __name__ == '__main__':
    unittest.main()
