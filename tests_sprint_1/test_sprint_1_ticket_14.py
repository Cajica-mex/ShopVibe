# test_sprint_1_ticket_14.py
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class TestSprint1Ticket14(unittest.TestCase):
    def test_parquet_ingestion_signature(self):
        try:
            from parquet_loader import cargar_parquet_a_sql
        except ImportError:
            self.fail("No se pudo importar cargar_parquet_a_sql desde parquet_loader")
            
        self.assertTrue(callable(cargar_parquet_a_sql))

if __name__ == '__main__':
    unittest.main()
