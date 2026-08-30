# test_sprint_1_ticket_11.py
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class TestSprint1Ticket11(unittest.TestCase):
    def test_address_normalization(self):
        try:
            from clean_data import normalizar_estado
        except ImportError:
            self.fail("No se pudo importar normalizar_estado desde clean_data")
            
        self.assertEqual(normalizar_estado("123 Main St, New York, NY, 10001"), "NY")
        self.assertEqual(normalizar_estado("Apartment, Los Angeles, CA"), "CA")
        self.assertEqual(normalizar_estado("No state listed here"), "UNKNOWN")

if __name__ == '__main__':
    unittest.main()
