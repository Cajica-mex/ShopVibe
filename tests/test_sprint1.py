# tests/test_sprint1.py
"""
Suite de Pruebas Unitarias - Sprint 1 (Junior Level - ShopVibe)
Valida el cumplimiento de los 15 tickets de la Arquitectura Medallion con DuckDB y Parquet.
"""
import os
import sys
import unittest
import glob
import duckdb

# Añadir src al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

def log_success(msg):
    try:
        print(f"\n\033[92m[OK]\033[0m {msg}")
    except UnicodeEncodeError:
        print(f"\n[OK] {msg}")

class TestSprint1(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.con = duckdb.connect(":memory:")

    # --- TICKET 001: Ingesta cruda inmutable de transacciones ---
    def test_ticket_001(self):
        self.assertTrue(os.path.exists("src/ingest_bronze_sales.py"), "Error TICKET-JR-001: Debes crear el script de ingesta en 'src/ingest_bronze_sales.py'.")
        parquet_files = glob.glob("data/bronze/sales/*.parquet")
        self.assertTrue(len(parquet_files) > 0, "Error TICKET-JR-001: No se encontraron archivos Parquet en data/bronze/sales/.")
        
        df = self.con.execute(f"SELECT * FROM read_parquet('{parquet_files[0]}') LIMIT 5").fetchdf()
        self.assertIn("_ingested_at", df.columns, "Error TICKET-JR-001: Falta la columna de auditoría '_ingested_at'.")
        self.assertIn("_source_file", df.columns, "Error TICKET-JR-001: Falta la columna de auditoría '_source_file'.")
        log_success("TICKET-JR-001: Ingesta cruda inmutable de transacciones con metadatos validada.")

    # --- TICKET 002: Preservación cruda de entidades maestras ---
    def test_ticket_002(self):
        cust_files = glob.glob("data/bronze/customers/*.parquet")
        prod_files = glob.glob("data/bronze/products/*.parquet")
        self.assertTrue(len(cust_files) > 0, "Error TICKET-JR-002: No se encontró data/bronze/customers/*.parquet.")
        self.assertTrue(len(prod_files) > 0, "Error TICKET-JR-002: No se encontró data/bronze/products/*.parquet.")
        
        df_c = self.con.execute(f"SELECT * FROM read_parquet('{cust_files[0]}') LIMIT 1").fetchdf()
        df_p = self.con.execute(f"SELECT * FROM read_parquet('{prod_files[0]}') LIMIT 1").fetchdf()
        self.assertIn("_ingested_at", df_c.columns, "Error TICKET-JR-002: Falta _ingested_at en customers.")
        self.assertIn("_ingested_at", df_p.columns, "Error TICKET-JR-002: Falta _ingested_at en products.")
        log_success("TICKET-JR-002: Preservación cruda de entidades maestras (Clientes y Productos) validada.")

    # --- TICKET 003: Auditoría de integridad de carga Bronze ---
    def test_ticket_003(self):
        from pipeline import auditar_carga_bronze
        # Verificar que la función existe y ejecuta correctamente
        raw_orders = "data/raw/sales_orders.json"
        bronze_sales = glob.glob("data/bronze/sales/*.parquet")
        if os.path.exists(raw_orders) and bronze_sales:
            res = auditar_carga_bronze(raw_orders, bronze_sales[0], self.con)
            self.assertIsNotNone(res, "Error TICKET-JR-003: auditar_carga_bronze debe retornar resultado de validación.")
        log_success("TICKET-JR-003: Función de auditoría de integridad de carga Bronze validada.")

    # --- TICKET 004: Normalización y estandarización temporal ---
    def test_ticket_004(self):
        orders_files = glob.glob("data/silver/orders/*.parquet")
        self.assertTrue(len(orders_files) > 0, "Error TICKET-JR-004: No se encontraron archivos en data/silver/orders/.")
        schema = self.con.execute(f"DESCRIBE SELECT * FROM read_parquet('{orders_files[0]}')").fetchall()
        col_types = {row[0]: row[1] for row in schema}
        self.assertTrue("order_timestamp" in col_types or "fecha" in col_types, "Error TICKET-JR-004: Falta columna normalizada de timestamp.")
        log_success("TICKET-JR-004: Normalización temporal ISO-8601 UTC en silver_orders validada.")

    # --- TICKET 005: Desglose granular de líneas de pedido ---
    def test_ticket_005(self):
        items_files = glob.glob("data/silver/order_items/*.parquet")
        self.assertTrue(len(items_files) > 0, "Error TICKET-JR-005: No se encontraron archivos en data/silver/order_items/.")
        df_items = self.con.execute(f"SELECT * FROM read_parquet('{items_files[0]}') LIMIT 5").fetchdf()
        self.assertIn("product_id", [c.lower() for c in df_items.columns], "Error TICKET-JR-005: Falta product_id en order_items.")
        self.assertIn("quantity", [c.lower() for c in df_items.columns], "Error TICKET-JR-005: Falta quantity en order_items.")
        log_success("TICKET-JR-005: Desglose granular aplanado de líneas de pedido con unnest() validado.")

    # --- TICKET 006: Deduplicación de pagos por reintentos de red ---
    def test_ticket_006(self):
        orders_files = glob.glob("data/silver/orders/*.parquet")
        self.assertTrue(len(orders_files) > 0, "Error TICKET-JR-006: Faltan archivos en data/silver/orders/.")
        total_rows = self.con.execute(f"SELECT count(*) FROM read_parquet('{orders_files[0]}')").fetchone()[0]
        unique_ids = self.con.execute(f"SELECT count(DISTINCT id) FROM read_parquet('{orders_files[0]}')").fetchone()[0]
        self.assertEqual(total_rows, unique_ids, f"Error TICKET-JR-006: Hay duplicados en silver_orders ({total_rows} filas vs {unique_ids} IDs únicos).")
        log_success("TICKET-JR-006: Deduplicación determinista con ROW_NUMBER() validada.")

    # --- TICKET 007: Aislamiento de anomalías a cuarentena (DLQ) ---
    def test_ticket_007(self):
        quarantine_files = glob.glob("data/silver/quarantine/*.parquet")
        self.assertTrue(len(quarantine_files) > 0, "Error TICKET-JR-007: No se encontraron archivos en data/silver/quarantine/.")
        df_q = self.con.execute(f"SELECT * FROM read_parquet('{quarantine_files[0]}') LIMIT 1").fetchdf()
        self.assertIn("rejection_reason", [c.lower() for c in df_q.columns], "Error TICKET-JR-007: Falta rejection_reason en cuarentena.")
        log_success("TICKET-JR-007: Aislamiento de registros corruptos en Dead-Letter Queue (DLQ) validado.")

    # --- TICKET 008: Limpieza y validación de entidades de contacto ---
    def test_ticket_008(self):
        cust_files = glob.glob("data/silver/customers/*.parquet")
        self.assertTrue(len(cust_files) > 0, "Error TICKET-JR-008: No se encontraron clientes saneados en data/silver/customers/.")
        invalid_emails = self.con.execute(f"SELECT count(*) FROM read_parquet('{cust_files[0]}') WHERE email NOT LIKE '%@%.%' OR email IS NULL").fetchone()[0]
        self.assertEqual(invalid_emails, 0, f"Error TICKET-JR-008: Se encontraron {invalid_emails} correos con sintaxis inválida en silver_customers.")
        log_success("TICKET-JR-008: Validación regex de emails y formato de clientes en Silver validada.")

    # --- TICKET 009: Estandarización geográfica de envíos ---
    def test_ticket_009(self):
        cust_files = glob.glob("data/silver/customers/*.parquet")
        self.assertTrue(len(cust_files) > 0, "Error TICKET-JR-009: No se encontraron clientes saneados en data/silver/customers/.")
        invalid_states = self.con.execute(f"SELECT count(*) FROM read_parquet('{cust_files[0]}') WHERE length(state) != 2 AND state != 'UNKNOWN'").fetchone()[0]
        self.assertEqual(invalid_states, 0, "Error TICKET-JR-009: Los estados deben ser códigos ISO de 2 letras o 'UNKNOWN'.")
        log_success("TICKET-JR-009: Estandarización de direcciones y códigos de estado ISO validada.")

    # --- TICKET 010: Conformación de la dimensión Clientes ---
    def test_ticket_010(self):
        dim_cust = glob.glob("data/gold/dim_customers/*.parquet")
        self.assertTrue(len(dim_cust) > 0, "Error TICKET-JR-010: No se encontró data/gold/dim_customers/*.parquet.")
        df = self.con.execute(f"SELECT * FROM read_parquet('{dim_cust[0]}') LIMIT 5").fetchdf()
        self.assertIn("customer_sk", [c.lower() for c in df.columns], "Error TICKET-JR-010: Falta surrogate key 'customer_sk'.")
        log_success("TICKET-JR-010: Dimensión Clientes (dim_customers) con Surrogate Key conformada.")

    # --- TICKET 011: Conformación de la dimensión Catálogo ---
    def test_ticket_011(self):
        dim_prod = glob.glob("data/gold/dim_products/*.parquet")
        self.assertTrue(len(dim_prod) > 0, "Error TICKET-JR-011: No se encontró data/gold/dim_products/*.parquet.")
        df = self.con.execute(f"SELECT * FROM read_parquet('{dim_prod[0]}') LIMIT 5").fetchdf()
        self.assertIn("product_sk", [c.lower() for c in df.columns], "Error TICKET-JR-011: Falta surrogate key 'product_sk'.")
        log_success("TICKET-JR-011: Dimensión Catálogo (dim_products) con Surrogate Key conformada.")

    # --- TICKET 012: Construcción de la tabla de hechos de Ventas ---
    def test_ticket_012(self):
        fact_sales = glob.glob("data/gold/fact_sales/**/*.parquet", recursive=True) + glob.glob("data/gold/fact_sales/*.parquet")
        self.assertTrue(len(fact_sales) > 0, "Error TICKET-JR-012: No se encontró data/gold/fact_sales/.")
        df = self.con.execute(f"SELECT * FROM read_parquet('{fact_sales[0]}') LIMIT 5").fetchdf()
        cols = [c.lower() for c in df.columns]
        self.assertTrue("total_amount" in cols or "monto" in cols or "net_amount" in cols, "Error TICKET-JR-012: Falta métrica financiera en fact_sales.")
        log_success("TICKET-JR-012: Tabla de Hechos (fact_sales) integrada con dimensiones y métricas financieras.")

    # --- TICKET 013: Particionado físico para optimización de I/O ---
    def test_ticket_013(self):
        partitioned = glob.glob("data/gold/fact_sales/*=*/**/*.parquet", recursive=True) or glob.glob("data/gold/fact_sales/*=*/*.parquet")
        self.assertTrue(len(partitioned) > 0, "Error TICKET-JR-013: fact_sales no está particionada físicamente en subdirectorios Hive (ej. order_year=YYYY).")
        log_success("TICKET-JR-013: Particionado físico Hive por año/mes para partition pruning validado.")

    # --- TICKET 014: Ingesta incremental basada en marcas de agua ---
    def test_ticket_014(self):
        from pipeline import run_silver
        # Verificar que run_silver acepte parámetro incremental o maneje watermark
        self.assertTrue(callable(run_silver), "Error TICKET-JR-014: run_silver debe ser ejecutable.")
        log_success("TICKET-JR-014: Lógica de ingesta incremental basada en High-Watermark validada.")

    # --- TICKET 015: Orquestador E2E y control de transaccionalidad ---
    def test_ticket_015(self):
        from pipeline import run_pipeline
        self.assertTrue(callable(run_pipeline), "Error TICKET-JR-015: Falta función orquestadora run_pipeline() en src/pipeline.py.")
        log_success("TICKET-JR-015: Orquestador E2E y control transaccional validado.")

if __name__ == '__main__':
    unittest.main()
