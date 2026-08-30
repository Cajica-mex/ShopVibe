# test_sprint_1_ticket_5.py
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class TestSprint1Ticket5(unittest.TestCase):
    def test_deduplication(self):
        try:
            from clean_data import eliminar_duplicados
        except ImportError:
            self.fail("No se pudo importar eliminar_duplicados desde clean_data")
            
        test_records = [
            {"id": 1, "val": "A"},
            {"id": 2, "val": "B"},
            {"id": 1, "val": "A"}
        ]
        res = eliminar_duplicados(test_records)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0]["id"], 1)
        self.assertEqual(res[1]["id"], 2)

if __name__ == '__main__':
    unittest.main()
