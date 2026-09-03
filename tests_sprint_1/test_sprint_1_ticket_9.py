# test_sprint_1_ticket_9.py
import os, sys, unittest, glob, duckdb

def log_success(msg):
    print(f"\n[OK] {msg}")

class TestTicket009(unittest.TestCase):
    def test_geographic_standardization(self):
        con = duckdb.connect(':memory:')
        cust_files = glob.glob('data/silver/customers/*.parquet')
        self.assertTrue(len(cust_files) > 0, "No se encontraron clientes saneados en data/silver/customers/.")
        invalid_states = con.execute(f"SELECT count(*) FROM read_parquet('{cust_files[0]}') WHERE length(state) != 2 AND state != 'UNKNOWN'").fetchone()[0]
        self.assertEqual(invalid_states, 0, "Los estados deben ser códigos ISO de 2 letras o 'UNKNOWN'.")
        log_success("TICKET-JR-009: Estandarización geográfica de envíos superada con éxito.")

if __name__ == '__main__':
    unittest.main()
