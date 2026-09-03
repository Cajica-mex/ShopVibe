# test_sprint_1_ticket_8.py
import os, sys, unittest, glob, duckdb

def log_success(msg):
    print(f"\n[OK] {msg}")

class TestTicket008(unittest.TestCase):
    def test_contact_cleansing(self):
        con = duckdb.connect(':memory:')
        cust_files = glob.glob('data/silver/customers/*.parquet')
        self.assertTrue(len(cust_files) > 0, "No se encontraron clientes saneados en data/silver/customers/.")
        invalid_emails = con.execute(f"SELECT count(*) FROM read_parquet('{cust_files[0]}') WHERE email NOT LIKE '%@%.%' OR email IS NULL").fetchone()[0]
        self.assertEqual(invalid_emails, 0, f"Se encontraron {invalid_emails} correos con formato inválido en silver_customers.")
        log_success("TICKET-JR-008: Limpieza y validación de entidades de contacto superada con éxito.")

if __name__ == '__main__':
    unittest.main()
