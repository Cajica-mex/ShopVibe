# test_sprint_1_ticket_6.py
import os, sys, unittest, glob, duckdb

def log_success(msg):
    print(f"\n[OK] {msg}")

class TestTicket006(unittest.TestCase):
    def test_deduplication(self):
        con = duckdb.connect(':memory:')
        orders_files = glob.glob('data/silver/orders/*.parquet')
        self.assertTrue(len(orders_files) > 0, "Faltan archivos en data/silver/orders/.")
        total_rows = con.execute(f"SELECT count(*) FROM read_parquet('{orders_files[0]}')").fetchone()[0]
        unique_ids = con.execute(f"SELECT count(DISTINCT id) FROM read_parquet('{orders_files[0]}')").fetchone()[0]
        self.assertEqual(total_rows, unique_ids, f"Hay duplicados en silver_orders ({total_rows} filas vs {unique_ids} IDs únicos).")
        log_success("TICKET-JR-006: Deduplicación determinista con ROW_NUMBER() superada con éxito.")

if __name__ == '__main__':
    unittest.main()
