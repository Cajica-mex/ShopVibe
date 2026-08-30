# test_sprint_1_ticket_7.py
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class TestSprint1Ticket7(unittest.TestCase):
    def test_date_standardization(self):
        try:
            from clean_data import estandarizar_fecha
        except ImportError:
            self.fail("No se pudo importar estandarizar_fecha desde clean_data")
            
        self.assertEqual(estandarizar_fecha("2026.08.20"), "2026-08-20")
        self.assertEqual(estandarizar_fecha("2026/08/20"), "2026-08-20")
        self.assertEqual(estandarizar_fecha("2026-08-20"), "2026-08-20")

if __name__ == '__main__':
    unittest.main()
