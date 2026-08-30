# test_sprint_1_ticket_15.py
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class TestSprint1Ticket15(unittest.TestCase):
    def test_pipeline_orchestrator_signature(self):
        try:
            from pipeline import ejecutar_pipeline_completo
        except ImportError:
            self.fail("No se pudo importar ejecutar_pipeline_completo desde pipeline")
            
        self.assertTrue(callable(ejecutar_pipeline_completo))

if __name__ == '__main__':
    unittest.main()
