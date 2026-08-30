# test_sprint_1_ticket_8.py
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class TestSprint1Ticket8(unittest.TestCase):
    def test_csv_delimiter_repair(self):
        try:
            from parse_csv import parsear_linea_csv
        except ImportError:
            self.fail("No se pudo importar parsear_linea_csv desde parse_csv")
            
        linea = '1,"Remera de Algodón, Classic Blue",25.99,Ropa'
        res = parsear_linea_csv(linea)
        self.assertEqual(len(res), 4)
        self.assertEqual(res[1], "Remera de Algodón, Classic Blue")

if __name__ == '__main__':
    unittest.main()
