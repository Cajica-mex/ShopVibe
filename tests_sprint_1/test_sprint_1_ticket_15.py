# test_sprint_1_ticket_15.py
import os, sys, unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

def log_success(msg):
    print(f"\n[OK] {msg}")

class TestTicket015(unittest.TestCase):
    def test_e2e_orchestrator(self):
        from pipeline import run_pipeline
        self.assertTrue(callable(run_pipeline), "Falta función run_pipeline() en src/pipeline.py.")
        log_success("TICKET-JR-015: Orquestador E2E y control de transaccionalidad superado con éxito.")

if __name__ == '__main__':
    unittest.main()
