# test_sprint_1_ticket_5.py
import os, sys, unittest, glob, duckdb

def log_success(msg):
    print(f"\n[OK] {msg}")

class TestTicket005(unittest.TestCase):
    def test_order_items_flattening(self):
        con = duckdb.connect(':memory:')
        items_files = glob.glob('data/silver/order_items/*.parquet')
        self.assertTrue(len(items_files) > 0, "No se encontraron archivos en data/silver/order_items/.")
        df = con.execute(f"SELECT * FROM read_parquet('{items_files[0]}') LIMIT 5").fetchdf()
        cols = [c.lower() for c in df.columns]
        self.assertIn('product_id', cols, "Falta product_id en order_items.")
        self.assertIn('quantity', cols, "Falta quantity en order_items.")
        log_success("TICKET-JR-005: Desglose granular aplanado con unnest() superado con éxito.")

if __name__ == '__main__':
    unittest.main()
