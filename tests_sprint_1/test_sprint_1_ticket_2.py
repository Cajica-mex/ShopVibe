# test_sprint_1_ticket_2.py
import os
import sys
import unittest

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

def log_success(msg):
    try:
        print(f"\n\033[92m✓\033[0m {msg}")
    except UnicodeEncodeError:
        print(f"\n\033[92m[OK]\033[0m {msg}")

class TestSprint1Ticket2(unittest.TestCase):
    
    def test_email_validation(self):
        try:
            from clean_data import es_correo_valido
        except ImportError:
            self.fail("No se pudo importar 'es_correo_valido' desde src/clean_data.py")
            
        self.assertTrue(es_correo_valido("juan.perez@example.com"))
        self.assertTrue(es_correo_valido("customer123@shopvibe.com"))
        self.assertFalse(es_correo_valido("invalid_email_no_at"))
        self.assertFalse(es_correo_valido(""))
        self.assertFalse(es_correo_valido(None))
        log_success("es_correo_valido valida correctamente correos estructurados y descarta inválidos o nulos.")

    def test_amount_validation(self):
        try:
            from clean_data import es_importe_valido
        except ImportError:
            self.fail("No se pudo importar 'es_importe_valido' desde src/clean_data.py")
            
        self.assertTrue(es_importe_valido(25.99))
        self.assertTrue(es_importe_valido(100))
        self.assertFalse(es_importe_valido(0))
        self.assertFalse(es_importe_valido(-15.50))
        self.assertFalse(es_importe_valido(None))
        log_success("es_importe_valido valida montos numéricos mayores a cero y descarta negativos o nulos.")

    def test_deduplication(self):
        try:
            from clean_data import eliminar_duplicados
        except ImportError:
            self.fail("No se pudo importar 'eliminar_duplicados' desde src/clean_data.py")
            
        records = [
            {"id": 1001, "item": "Jeans"},
            {"id": 1002, "item": "Gorra"},
            {"id": 1001, "item": "Jeans (Duplicado)"}
        ]
        deduped = eliminar_duplicados(records)
        self.assertEqual(len(deduped), 2, "La lista debe contener exactamente 2 registros únicos.")
        self.assertEqual(deduped[0]["id"], 1001)
        self.assertEqual(deduped[1]["id"], 1002)
        log_success("eliminar_duplicados elimina registros repetidos preservando el primer registro único.")

    def test_flatten_nested_order(self):
        try:
            from clean_data import aplanar_orden
        except ImportError:
            self.fail("No se pudo importar 'aplanar_orden' desde src/clean_data.py")
            
        order = {
            "id": 1050,
            "cliente_id": 12,
            "fecha": "2026-08-20",
            "articulos": [
                {"producto_id": 1, "cantidad": 2, "precio": 25.0},
                {"producto_id": 3, "cantidad": 1, "precio": 80.0}
            ]
        }
        flat_rows = aplanar_orden(order)
        self.assertEqual(len(flat_rows), 2, "Se esperaban 2 filas aplanadas a partir de los artículos de la orden.")
        self.assertEqual(flat_rows[0]["id_orden"], 1050)
        self.assertEqual(flat_rows[0]["monto"], 50.0)
        self.assertEqual(flat_rows[1]["monto"], 80.0)
        log_success("aplanar_orden desanida correctamente listas de artículos en filas individuales con montos calculados.")

    def test_date_standardization(self):
        try:
            from clean_data import estandarizar_fecha
        except ImportError:
            self.fail("No se pudo importar 'estandarizar_fecha' desde src/clean_data.py")
            
        self.assertEqual(estandarizar_fecha("2026.08.20"), "2026-08-20")
        self.assertEqual(estandarizar_fecha("2026/08/20"), "2026-08-20")
        self.assertEqual(estandarizar_fecha("2026-08-20"), "2026-08-20")
        log_success("estandarizar_fecha homologa formatos de fecha heterogéneos al estándar ISO YYYY-MM-DD.")

    def test_state_normalization(self):
        try:
            from clean_data import normalizar_estado
        except ImportError:
            self.fail("No se pudo importar 'normalizar_estado' desde src/clean_data.py")
            
        self.assertEqual(normalizar_estado("123 Main St, New York, NY, 10001"), "NY")
        self.assertEqual(normalizar_estado("Apartment 4B, Los Angeles, CA"), "CA")
        self.assertEqual(normalizar_estado("No valid state provided"), "UNKNOWN")
        log_success("normalizar_estado extrae códigos de estado válidos de direcciones o asigna UNKNOWN.")

    def test_contract_schema_validation(self):
        try:
            from clean_data import validar_contrato
        except ImportError:
            self.fail("No se pudo importar 'validar_contrato' desde src/clean_data.py")
            
        schema = {"id": int, "nombre": str, "precio": float}
        self.assertTrue(validar_contrato({"id": 1, "nombre": "Buzo", "precio": 45.0}, schema))
        self.assertFalse(validar_contrato({"id": "no-int", "nombre": "Buzo", "precio": 45.0}, schema))
        self.assertFalse(validar_contrato({"id": 1, "nombre": "Buzo"}, schema))
        log_success("validar_contrato verifica estrictamente campos requeridos y tipos de datos del esquema.")

    def test_csv_quoted_delimiters(self):
        try:
            from parse_csv import parsear_linea_csv
        except ImportError:
            self.fail("No se pudo importar 'parsear_linea_csv' desde src/parse_csv.py")
            
        line = '1,"Remera de Algodón, Classic Blue",25.99,Ropa'
        parsed = parsear_linea_csv(line)
        self.assertEqual(len(parsed), 4, "La línea CSV debe parsearse en exactamente 4 columnas.")
        self.assertEqual(parsed[1], "Remera de Algodón, Classic Blue")
        log_success("parsear_linea_csv procesa adecuadamente campos entrecomillados con comas internas sin romper columnas.")

    def test_audit_quarantine_logging(self):
        try:
            from audit import registrar_descarte
        except ImportError:
            self.fail("No se pudo importar 'registrar_descarte' desde src/audit.py")
            
        log_file = "descartes.log"
        if os.path.exists(log_file):
            os.remove(log_file)
            
        registrar_descarte("EMAIL_INVALIDO", {"id": 999, "email": "corrupt_data"})
        self.assertTrue(os.path.exists(log_file), "No se creó el archivo de auditoría descartes.log.")
        
        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        self.assertIn("EMAIL_INVALIDO", content)
        self.assertIn("corrupt_data", content)
        
        if os.path.exists(log_file):
            os.remove(log_file)
            
        log_success("registrar_descarte persiste los fallos de calidad y registros corruptos en descartes.log.")

if __name__ == '__main__':
    unittest.main()
