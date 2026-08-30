# test_sprint_1_ticket_10.py
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class TestSprint1Ticket10(unittest.TestCase):
    def test_schema_contract(self):
        try:
            from clean_data import validar_contrato
        except ImportError:
            self.fail("No se pudo importar validar_contrato desde clean_data")
            
        esquema = {"id": int, "name": str}
        self.assertTrue(validar_contrato({"id": 1, "name": "shirt"}, esquema))
        self.assertFalse(validar_contrato({"id": "one", "name": "shirt"}, esquema))
        self.assertFalse(validar_contrato({"name": "shirt"}, esquema))

if __name__ == '__main__':
    unittest.main()
