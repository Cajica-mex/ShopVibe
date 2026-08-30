# test_sprint_1_ticket_4.py
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class TestSprint1Ticket4(unittest.TestCase):
    def test_amount_validation(self):
        try:
            from clean_data import es_importe_valido
        except ImportError:
            self.fail("No se pudo importar es_importe_valido desde clean_data")
            
        self.assertTrue(es_importe_valido(25.99))
        self.assertFalse(es_importe_valido(0))
        self.assertFalse(es_importe_valido(-10.5))
        self.assertFalse(es_importe_valido(None))

if __name__ == '__main__':
    unittest.main()
