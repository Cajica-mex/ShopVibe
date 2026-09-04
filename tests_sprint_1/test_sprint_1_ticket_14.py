# test_sprint_1_ticket_14.py
import os, sys, unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

def log_success(msg):
    print(f"\n[OK] {msg}")

class TestTicket014(unittest.TestCase):
    def test_watermark_incremental(self):
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/incremental_orders.py'))
        self.assertTrue(os.path.exists(script_path), f"Error TICKET-JR-014: Debes crear el script 'src/incremental_orders.py'.")
        
        from incremental_orders import run_incremental as inc_func
        self.assertTrue(callable(inc_func), "La función run_incremental debe estar definida y ser ejecutable.")
        
        # Test executing watermark logic
        res = inc_func(watermark='2026-08-25')
        self.assertIsNotNone(res, "run_incremental debe retornar los registros procesados para la marca de agua.")
        log_success("TICKET-JR-014: Ingesta incremental basada en marcas de agua superada con éxito.")

if __name__ == '__main__':
    unittest.main()
