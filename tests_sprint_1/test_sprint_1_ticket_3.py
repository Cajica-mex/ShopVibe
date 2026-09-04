# test_sprint_1_ticket_3.py
import os, sys, unittest, glob, duckdb
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

def log_success(msg):
    print(f"\n[OK] {msg}")

class TestTicket003(unittest.TestCase):
    def test_integrity_audit(self):
        try:
            from audit_bronze import auditar_carga_bronze
        except ImportError:
            from pipeline import auditar_carga_bronze
        con = duckdb.connect(':memory:')
        raw_orders = 'data/raw/sales_orders.json'
        bronze_sales = glob.glob('data/bronze/sales/*.parquet')
        self.assertTrue(os.path.exists(raw_orders), "No existe archivo crudo.")
        self.assertTrue(len(bronze_sales) > 0, "No existe archivo Parquet en Bronze.")
        res = auditar_carga_bronze(raw_orders, bronze_sales[0], con)
        self.assertIsNotNone(res, "auditar_carga_bronze debe retornar resultado de validación.")
        log_success("TICKET-JR-003: Auditoría de integridad de carga Bronze superada con éxito.")

if __name__ == '__main__':
    unittest.main()
