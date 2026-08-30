# test_sprint_1_ticket_3.py
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class TestSprint1Ticket3(unittest.TestCase):
    def test_email_validation(self):
        try:
            from clean_data import es_correo_valido
        except ImportError:
            self.fail("No se pudo importar es_correo_valido desde clean_data")
            
        self.assertTrue(es_correo_valido("test@shopvibe.com"))
        self.assertFalse(es_correo_valido("invalid_email"))
        self.assertFalse(es_correo_valido(""))
        self.assertFalse(es_correo_valido(None))

if __name__ == '__main__':
    unittest.main()
