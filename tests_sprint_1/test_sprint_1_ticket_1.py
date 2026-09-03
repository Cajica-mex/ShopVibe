# test_sprint_1_ticket_1.py
import os, sys, unittest, glob, duckdb

def log_success(msg):
    print(f"\n[OK] {msg}")

class TestTicket001(unittest.TestCase):
    def test_bronze_sales_ingestion(self):
        con = duckdb.connect(':memory:')
        parquet_files = glob.glob('data/bronze/sales/*.parquet')
        self.assertTrue(len(parquet_files) > 0, "Error TICKET-JR-001: No se encontraron archivos Parquet en data/bronze/sales/.")
        df = con.execute(f"SELECT * FROM read_parquet('{parquet_files[0]}') LIMIT 5").fetchdf()
        self.assertIn('_ingested_at', df.columns, "Error TICKET-JR-001: Falta la columna '_ingested_at'.")
        self.assertIn('_source_file', df.columns, "Error TICKET-JR-001: Falta la columna '_source_file'.")
        log_success("TICKET-JR-001: Ingesta cruda inmutable de transacciones con metadatos superada con éxito.")

if __name__ == '__main__':
    unittest.main()
