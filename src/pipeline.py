# src/pipeline.py
"""
ShopVibe - Data Engineering Pipeline E2E
Arquitectura Medallion (Bronze -> Silver -> Gold) con DuckDB y Parquet.
"""
import os
import sys
import duckdb

def get_connection(db_path=":memory:"):
    return duckdb.connect(db_path)

# --- CAPA BRONZE (TICKETS 001 - 003) ---
def run_bronze(con=None):
    """
    Ingesta inmutable cruda de archivos JSON y CSV a Parquet con metadatos.
    """
    if con is None:
        con = get_connection()
    os.makedirs("data/bronze/sales", exist_ok=True)
    os.makedirs("data/bronze/customers", exist_ok=True)
    os.makedirs("data/bronze/products", exist_ok=True)

    # TODO (TICKET-JR-001): Ingestar sales_orders.json a data/bronze/sales/ con _ingested_at y _source_file
    # TODO (TICKET-JR-002): Ingestar customers.csv y products.csv a data/bronze/customers/ y products/
    pass

def auditar_carga_bronze(source_path, target_path, con=None):
    """
    TODO (TICKET-JR-003): Auditar que el conteo en source_path sea idéntico al de target_path.
    """
    pass

# --- CAPA SILVER (TICKETS 004 - 009) ---
def run_silver(con=None):
    """
    Normalización temporal, aplanamiento, deduplicación, cuarentena y validación.
    """
    if con is None:
        con = get_connection()
    os.makedirs("data/silver/orders", exist_ok=True)
    os.makedirs("data/silver/order_items", exist_ok=True)
    os.makedirs("data/silver/customers", exist_ok=True)
    os.makedirs("data/silver/quarantine", exist_ok=True)

    # TODO (TICKET-JR-004): Normalización de fechas a ISO-8601 UTC en silver_orders
    # TODO (TICKET-JR-005): Aplanar articulos con unnest() en silver_order_items
    # TODO (TICKET-JR-006): Deduplicar pedidos con ROW_NUMBER()
    # TODO (TICKET-JR-007): Desviar anomalías a silver_quarantine
    # TODO (TICKET-JR-008): Limpieza y regex de emails en silver_customers
    # TODO (TICKET-JR-009): Normalización de direcciones y códigos de estado ISO
    pass

# --- CAPA GOLD & INCREMENTAL (TICKETS 010 - 014) ---
def run_gold(con=None):
    """
    Conformación del Star Schema (dim_customers, dim_products, fact_sales) y particionado.
    """
    if con is None:
        con = get_connection()
    os.makedirs("data/gold/dim_customers", exist_ok=True)
    os.makedirs("data/gold/dim_products", exist_ok=True)
    os.makedirs("data/gold/fact_sales", exist_ok=True)

    # TODO (TICKET-JR-010): Conformar dim_customers con surrogate key (customer_sk)
    # TODO (TICKET-JR-011): Conformar dim_products con surrogate key (product_sk)
    # TODO (TICKET-JR-012): Construir fact_sales calculando importes netos
    # TODO (TICKET-JR-013): Particionar físicamente fact_sales por año y mes
    pass

# --- ORQUESTADOR PRINCIPAL (TICKET 015) ---
def run_pipeline():
    """
    TODO (TICKET-JR-015): Orquestador secuencial Bronze -> Silver -> Gold con try/except y logs.
    """
    print("Iniciando pipeline Medallion de ShopVibe...")
    con = get_connection()
    try:
        run_bronze(con)
        run_silver(con)
        run_gold(con)
        print("Pipeline completado exitosamente.")
    except Exception as e:
        print(f"Error crítico en la ejecución del pipeline: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()
