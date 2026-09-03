# test_sprint_1_ticket_12.py
import os, sys, unittest, glob, duckdb

def log_success(msg):
    print(f"\n[OK] {msg}")

class TestTicket012(unittest.TestCase):
    def test_fact_sales_construction(self):
        con = duckdb.connect(':memory:')
        fact_sales = glob.glob('data/gold/fact_sales/**/*.parquet', recursive=True) + glob.glob('data/gold/fact_sales/*.parquet')
        self.assertTrue(len(fact_sales) > 0, "No se encontró data/gold/fact_sales/.")
        df = con.execute(f"SELECT * FROM read_parquet('{fact_sales[0]}') LIMIT 5").fetchdf()
        cols = [c.lower() for c in df.columns]
        self.assertTrue('total_amount' in cols or 'monto' in cols or 'net_amount' in cols, "Falta métrica financiera en fact_sales.")
        log_success("TICKET-JR-012: Construcción de la tabla de hechos de Ventas superada con éxito.")

if __name__ == '__main__':
    unittest.main()
