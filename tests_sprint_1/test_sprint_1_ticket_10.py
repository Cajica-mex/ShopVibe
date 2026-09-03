# test_sprint_1_ticket_10.py
import os, sys, unittest, glob, duckdb

def log_success(msg):
    print(f"\n[OK] {msg}")

class TestTicket010(unittest.TestCase):
    def test_dim_customers_conformation(self):
        con = duckdb.connect(':memory:')
        dim_cust = glob.glob('data/gold/dim_customers/*.parquet')
        self.assertTrue(len(dim_cust) > 0, "No se encontró data/gold/dim_customers/*.parquet.")
        df = con.execute(f"SELECT * FROM read_parquet('{dim_cust[0]}') LIMIT 5").fetchdf()
        self.assertIn('customer_sk', [c.lower() for c in df.columns], "Falta surrogate key 'customer_sk'.")
        log_success("TICKET-JR-010: Conformación de la dimensión Clientes con Surrogate Key superada con éxito.")

if __name__ == '__main__':
    unittest.main()
