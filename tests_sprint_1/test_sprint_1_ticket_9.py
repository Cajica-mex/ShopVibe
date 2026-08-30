# test_sprint_1_ticket_9.py
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class TestSprint1Ticket9(unittest.TestCase):
    def test_dead_letter_logging(self):
        try:
            from audit import registrar_descarte
        except ImportError:
            self.fail("No se pudo importar registrar_descarte desde audit")
            
        log_file = "descartes.log"
        if os.path.exists(log_file):
            os.remove(log_file)
            
        registrar_descarte("EMAIL_INVALIDO", {"id": 9, "email": "bad"})
        self.assertTrue(os.path.exists(log_file))
        with open(log_file, 'r') as f:
            content = f.read()
        self.assertIn("EMAIL_INVALIDO", content)
        self.assertIn("bad", content)
        
        if os.path.exists(log_file):
            os.remove(log_file)

if __name__ == '__main__':
    unittest.main()
