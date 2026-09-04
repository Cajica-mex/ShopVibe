# test_sprint_1_ticket_1.py
import os, sys, unittest, glob, duckdb

def log_success(msg):
    print(f"\n[OK] {msg}")

class TestTicket001(unittest.TestCase):
    def test_bronze_sales_ingestion(self):
        con = duckdb.connect(':memory:')
        
        # 1. Validar que el script de ingesta fue creado
        script_path = 'src/ingest_bronze_sales.py'
        self.assertTrue(os.path.exists(script_path), f"Error TICKET-JR-001: Debes crear el script de ingesta en '{script_path}'.")
        log_success("Archivo src/ingest_bronze_sales.py creado correctamente.")

        # 2. Validar que los archivos Parquet se generaron en la capa Bronze
        parquet_files = glob.glob('data/bronze/sales/*.parquet')
        self.assertTrue(len(parquet_files) > 0, "Error TICKET-JR-001: No se encontraron archivos Parquet en data/bronze/sales/.")
        log_success("Archivos Parquet generados en data/bronze/sales/.")

        # 3. Validar esquema y metadatos de auditoría obligatorios
        df = con.execute(f"SELECT * FROM read_parquet('{parquet_files[0]}') LIMIT 5").fetchdf()
        self.assertIn('_ingested_at', df.columns, "Error TICKET-JR-001: Falta la columna de auditoría '_ingested_at'.")
        self.assertIn('_source_file', df.columns, "Error TICKET-JR-001: Falta la columna de auditoría '_source_file'.")
        log_success("Metadatos de auditoría (_ingested_at, _source_file) validados.")
        log_success("TICKET-JR-001: Ingesta cruda inmutable de transacciones completada con éxito.")

if __name__ == '__main__':
    unittest.main()
