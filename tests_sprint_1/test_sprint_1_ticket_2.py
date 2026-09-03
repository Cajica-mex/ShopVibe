# test_sprint_1_ticket_2.py
import os, sys, unittest, glob, duckdb

def log_success(msg):
    print(f"\n[OK] {msg}")

class TestTicket002(unittest.TestCase):
    def test_bronze_master_entities(self):
        con = duckdb.connect(':memory:')
        cust_files = glob.glob('data/bronze/customers/*.parquet')
        prod_files = glob.glob('data/bronze/products/*.parquet')
        self.assertTrue(len(cust_files) > 0, "Error TICKET-JR-002: No se encontró data/bronze/customers/*.parquet.")
        self.assertTrue(len(prod_files) > 0, "Error TICKET-JR-002: No se encontró data/bronze/products/*.parquet.")
        df_c = con.execute(f"SELECT * FROM read_parquet('{cust_files[0]}') LIMIT 1").fetchdf()
        df_p = con.execute(f"SELECT * FROM read_parquet('{prod_files[0]}') LIMIT 1").fetchdf()
        self.assertIn('_ingested_at', df_c.columns, "Error TICKET-JR-002: Falta _ingested_at en customers.")
        self.assertIn('_ingested_at', df_p.columns, "Error TICKET-JR-002: Falta _ingested_at en products.")
        log_success("TICKET-JR-002: Preservación cruda de entidades maestras (Clientes y Productos) superada con éxito.")

if __name__ == '__main__':
    unittest.main()
