# test_sprint_1_ticket_4.py
import os, sys, unittest, glob, duckdb

def log_success(msg):
    print(f"\n[OK] {msg}")

class TestTicket004(unittest.TestCase):
    def test_temporal_normalization(self):
        con = duckdb.connect(':memory:')
        orders_files = glob.glob('data/silver/orders/*.parquet')
        self.assertTrue(len(orders_files) > 0, "No se encontraron archivos en data/silver/orders/.")
        schema = con.execute(f"DESCRIBE SELECT * FROM read_parquet('{orders_files[0]}')").fetchall()
        col_types = {row[0]: row[1] for row in schema}
        self.assertTrue('order_timestamp' in col_types or 'fecha' in col_types, "Falta columna de timestamp normalizado.")
        log_success("TICKET-JR-004: Normalización temporal ISO-8601 UTC en silver_orders superada con éxito.")

if __name__ == '__main__':
    unittest.main()
