# test_sprint1.py
import os
import sys
import unittest
import sqlite3

# Add src to python path dynamically
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class TestSprint1(unittest.TestCase):
    
    # --- TICKET 001 & 002: DDL Verification ---
    def test_ticket_001_002_database_ddl(self):
        db_path = "test_academy.db"
        if os.path.exists(db_path):
            os.remove(db_path)
            
        conn = sqlite3.connect(db_path)
        schema_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../schema.sql'))
        
        # Read and execute schema
        with open(schema_path, 'r', encoding='utf-8') as f:
            sql = f.read()
            
        try:
            conn.executescript(sql)
            conn.commit()
        except Exception as e:
            conn.close()
            if os.path.exists(db_path):
                os.remove(db_path)
            self.fail(f"Falla al ejecutar schema.sql: {str(e)}")
            
        cursor = conn.cursor()
        
        # Verify dim_products
        try:
            cursor.execute("SELECT id, product_name, price, category FROM dim_products")
        except sqlite3.OperationalError as e:
            conn.close()
            if os.path.exists(db_path):
                os.remove(db_path)
            self.fail(f"dim_products no tiene las columnas requeridas o no existe: {str(e)}")
            
        # Verify dim_customers
        try:
            cursor.execute("SELECT id, customer_name, email FROM dim_customers")
        except sqlite3.OperationalError as e:
            conn.close()
            if os.path.exists(db_path):
                os.remove(db_path)
            self.fail(f"dim_customers no tiene las columnas requeridas o no existe: {str(e)}")
            
        # Verify fact_sales
        try:
            cursor.execute("SELECT id, customer_id, product_id, quantity, sale_date, total_amount FROM fact_sales")
        except sqlite3.OperationalError as e:
            conn.close()
            if os.path.exists(db_path):
                os.remove(db_path)
            self.fail(f"fact_sales no tiene las columnas requeridas o no existe: {str(e)}")
            
        conn.close()
        if os.path.exists(db_path):
            os.remove(db_path)

    # --- TICKET 003: Email Validation ---
    def test_ticket_003_email_validation(self):
        try:
            from clean_data import es_correo_valido
        except ImportError:
            self.fail("No se pudo importar es_correo_valido desde clean_data")
            
        self.assertTrue(es_correo_valido("test@shopvibe.com"))
        self.assertFalse(es_correo_valido("invalid_email"))
        self.assertFalse(es_correo_valido(""))
        self.assertFalse(es_correo_valido(None))

    # --- TICKET 004: Amount Validation ---
    def test_ticket_004_amount_validation(self):
        try:
            from clean_data import es_importe_valido
        except ImportError:
            self.fail("No se pudo importar es_importe_valido desde clean_data")
            
        self.assertTrue(es_importe_valido(25.99))
        self.assertFalse(es_importe_valido(0))
        self.assertFalse(es_importe_valido(-10.5))
        self.assertFalse(es_importe_valido(None))

    # --- TICKET 005: Deduplication ---
    def test_ticket_005_deduplication(self):
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

    # --- TICKET 006: Flattening ---
    def test_ticket_006_flattening(self):
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

    # --- TICKET 007: Date Standardization ---
    def test_ticket_007_date_standardization(self):
        try:
            from clean_data import estandarizar_fecha
        except ImportError:
            self.fail("No se pudo importar estandarizar_fecha desde clean_data")
            
        self.assertEqual(estandarizar_fecha("2026.08.20"), "2026-08-20")
        self.assertEqual(estandarizar_fecha("2026/08/20"), "2026-08-20")
        self.assertEqual(estandarizar_fecha("2026-08-20"), "2026-08-20")

    # --- TICKET 008: CSV Delimiter Repair ---
    def test_ticket_008_csv_delimiter_repair(self):
        try:
            from parse_csv import parsear_linea_csv
        except ImportError:
            self.fail("No se pudo importar parsear_linea_csv desde parse_csv")
            
        linea = '1,"Remera de Algodón, Classic Blue",25.99,Ropa'
        res = parsear_linea_csv(linea)
        self.assertEqual(len(res), 4)
        self.assertEqual(res[1], "Remera de Algodón, Classic Blue")

    # --- TICKET 009: Dead Letter Logging ---
    def test_ticket_009_dead_letter_logging(self):
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

    # --- TICKET 010: Schema Contract Validation ---
    def test_ticket_010_schema_contract(self):
        try:
            from clean_data import validar_contrato
        except ImportError:
            self.fail("No se pudo importar validar_contrato desde clean_data")
            
        esquema = {"id": int, "name": str}
        self.assertTrue(validar_contrato({"id": 1, "name": "shirt"}, esquema))
        self.assertFalse(validar_contrato({"id": "one", "name": "shirt"}, esquema))
        self.assertFalse(validar_contrato({"name": "shirt"}, esquema))

    # --- TICKET 011: Address Normalization ---
    def test_ticket_011_address_normalization(self):
        try:
            from clean_data import normalizar_estado
        except ImportError:
            self.fail("No se pudo importar normalizar_estado desde clean_data")
            
        self.assertEqual(normalizar_estado("123 Main St, New York, NY, 10001"), "NY")
        self.assertEqual(normalizar_estado("Apartment, Los Angeles, CA"), "CA")
        self.assertEqual(normalizar_estado("No state listed here"), "UNKNOWN")

    # --- TICKET 012 & 013: Incremental & Unique Ingestion ---
    def test_ticket_012_013_db_loading(self):
        try:
            from db_loader import cargar_incremental, insertar_con_control
        except ImportError:
            self.fail("No se pudo importar de db_loader")
            
        db_path = "test_loader.db"
        if os.path.exists(db_path):
            os.remove(db_path)
            
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE fact_sales (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                sale_date TEXT,
                total_amount REAL
            )
        """)
        conn.commit()
        
        test_records = [
            {"id": 201, "customer_id": 1, "product_id": 2, "quantity": 1, "fecha": "2026-08-20", "monto": 10.0},
            {"id": 202, "customer_id": 2, "product_id": 3, "quantity": 2, "fecha": "2026-08-20", "monto": 30.0}
        ]
        
        # Test incremental load
        cargar_incremental(conn, test_records)
        cursor.execute("SELECT COUNT(*) FROM fact_sales")
        self.assertEqual(cursor.fetchone()[0], 2)
        
        # Test unique control
        dup_record = {"id": 201, "customer_id": 1, "product_id": 2, "quantity": 1, "fecha": "2026-08-20", "monto": 10.0}
        insertar_con_control(conn, dup_record)
        cursor.execute("SELECT COUNT(*) FROM fact_sales")
        self.assertEqual(cursor.fetchone()[0], 2)  # Should not increase since 201 exists
        
        conn.close()
        if os.path.exists(db_path):
            os.remove(db_path)

    # --- TICKET 014: Parquet Ingestion ---
    def test_ticket_014_parquet_ingestion(self):
        try:
            from parquet_loader import cargar_parquet_a_sql
        except ImportError:
            self.fail("No se pudo importar cargar_parquet_a_sql desde parquet_loader")
            
        # This test checks if import and definition are ready
        self.assertTrue(callable(cargar_parquet_a_sql))

    # --- TICKET 015: E2E Pipeline Orchestrator ---
    def test_ticket_015_e2e_pipeline(self):
        try:
            from pipeline import ejecutar_pipeline_completo
        except ImportError:
            self.fail("No se pudo importar ejecutar_pipeline_completo desde pipeline")
            
        # Verify callability
        self.assertTrue(callable(ejecutar_pipeline_completo))

if __name__ == '__main__':
    unittest.main()
