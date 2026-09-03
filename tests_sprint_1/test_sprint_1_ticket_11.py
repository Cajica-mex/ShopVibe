# test_sprint_1_ticket_11.py
import os, sys, unittest, glob, duckdb

def log_success(msg):
    print(f"\n[OK] {msg}")

class TestTicket011(unittest.TestCase):
    def test_dim_products_conformation(self):
        con = duckdb.connect(':memory:')
        dim_prod = glob.glob('data/gold/dim_products/*.parquet')
        self.assertTrue(len(dim_prod) > 0, "No se encontró data/gold/dim_products/*.parquet.")
        df = con.execute(f"SELECT * FROM read_parquet('{dim_prod[0]}') LIMIT 5").fetchdf()
        self.assertIn('product_sk', [c.lower() for c in df.columns], "Falta surrogate key 'product_sk'.")
        log_success("TICKET-JR-011: Conformación de la dimensión Catálogo con Surrogate Key superada con éxito.")

if __name__ == '__main__':
    unittest.main()
