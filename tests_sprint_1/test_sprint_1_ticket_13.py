# test_sprint_1_ticket_13.py
import os, sys, unittest, glob, duckdb

def log_success(msg):
    print(f"\n[OK] {msg}")

class TestTicket013(unittest.TestCase):
    def test_physical_partitioning(self):
        partitioned = glob.glob('data/gold/fact_sales/*=*/**/*.parquet', recursive=True) or glob.glob('data/gold/fact_sales/*=*/*.parquet')
        self.assertTrue(len(partitioned) > 0, "fact_sales no está particionada físicamente en subdirectorios Hive (ej. order_year=YYYY).")
        log_success("TICKET-JR-013: Particionado físico para optimización de I/O superado con éxito.")

if __name__ == '__main__':
    unittest.main()
