# test_sprint_1_ticket_7.py
import os, sys, unittest, glob, duckdb

def log_success(msg):
    print(f"\n[OK] {msg}")

class TestTicket007(unittest.TestCase):
    def test_quarantine_dlq(self):
        con = duckdb.connect(':memory:')
        quarantine_files = glob.glob('data/silver/quarantine/*.parquet')
        self.assertTrue(len(quarantine_files) > 0, "No se encontraron archivos en data/silver/quarantine/.")
        df = con.execute(f"SELECT * FROM read_parquet('{quarantine_files[0]}') LIMIT 1").fetchdf()
        self.assertIn('rejection_reason', [c.lower() for c in df.columns], "Falta rejection_reason en cuarentena.")
        log_success("TICKET-JR-007: Aislamiento de anomalías a cuarentena (DLQ) superado con éxito.")

if __name__ == '__main__':
    unittest.main()
