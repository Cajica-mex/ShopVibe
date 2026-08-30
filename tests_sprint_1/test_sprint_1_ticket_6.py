# test_sprint_1_ticket_6.py
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class TestSprint1Ticket6(unittest.TestCase):
    def test_flattening(self):
        try:
            from clean_data import aplanar_orden
        except ImportError:
            self.fail("No se pudo importar aplanar_orden desde clean_data")
            
        test_order = {
            "id": 500,
            "cliente_id": 9,
            "fecha": "2026-08-20",
            "articulos": [
                {"producto_id": 2, "cantidad": 2, "precio": 10.0},
                {"producto_id": 3, "cantidad": 1, "precio": 15.0}
            ]
        }
        res = aplanar_orden(test_order)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0]["monto"], 20.0)
        self.assertEqual(res[1]["monto"], 15.0)
        self.assertEqual(res[0]["cliente_id"], 9)
        self.assertEqual(res[0]["id_orden"], 500)

if __name__ == '__main__':
    unittest.main()
