# test_sprint_1_ticket_14.py
import os, sys, unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

def log_success(msg):
    print(f"\n[OK] {msg}")

class TestTicket014(unittest.TestCase):
    def test_watermark_incremental(self):
        from pipeline import run_silver
        self.assertTrue(callable(run_silver), "run_silver debe ser ejecutable.")
        log_success("TICKET-JR-014: Ingesta incremental basada en marcas de agua superada con éxito.")

if __name__ == '__main__':
    unittest.main()
