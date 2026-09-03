-- ShopVibe Analytic Warehouse - DuckDB DDL Definitions (schema.sql)
-- Medallion Architecture: Bronze (Raw Parquet) -> Silver (Clean Tables/Views) -> Gold (Star Schema)

-- =========================================================================
-- --- SILVER LAYER (Clean & Normalized Tables) ---
-- =========================================================================

-- silver_orders: Pedidos saneados con timestamps estandarizados UTC
CREATE TABLE IF NOT EXISTS silver_orders (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER,
    cliente_name VARCHAR,
    email VARCHAR,
    order_timestamp TIMESTAMP,
    _ingested_at TIMESTAMP,
    _source_file VARCHAR
);

-- silver_order_items: Desglose granular aplanado de cada línea de pedido
CREATE TABLE IF NOT EXISTS silver_order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price DOUBLE,
    line_total DOUBLE
);

-- silver_customers: Directorio de clientes con correos validados y estado ISO de 2 letras
CREATE TABLE IF NOT EXISTS silver_customers (
    id INTEGER PRIMARY KEY,
    customer_name VARCHAR,
    email VARCHAR,
    address VARCHAR,
    state VARCHAR(2),
    signup_date DATE
);

-- silver_products: Catálogo depurado de productos
CREATE TABLE IF NOT EXISTS silver_products (
    id INTEGER PRIMARY KEY,
    product_name VARCHAR,
    price DOUBLE,
    category VARCHAR
);

-- silver_quarantine: Dead-Letter Queue (DLQ) para compras con anomalías
CREATE TABLE IF NOT EXISTS silver_quarantine (
    id INTEGER,
    cliente_id INTEGER,
    monto DOUBLE,
    rejection_reason VARCHAR,
    rejected_at TIMESTAMP
);

-- =========================================================================
-- --- GOLD LAYER (Star Schema - Dimensional Model) ---
-- =========================================================================

-- dim_customers: Dimensión Clientes con Surrogate Key
CREATE TABLE IF NOT EXISTS dim_customers (
    customer_sk VARCHAR PRIMARY KEY,
    customer_id INTEGER,
    customer_name VARCHAR,
    email VARCHAR,
    state VARCHAR(2),
    signup_date DATE
);

-- dim_products: Dimensión Productos con Surrogate Key
CREATE TABLE IF NOT EXISTS dim_products (
    product_sk VARCHAR PRIMARY KEY,
    product_id INTEGER,
    product_name VARCHAR,
    price DOUBLE,
    category VARCHAR
);

-- fact_sales: Tabla de Hechos de Ventas vinculada por Surrogate Keys
CREATE TABLE IF NOT EXISTS fact_sales (
    order_id INTEGER,
    customer_sk VARCHAR,
    product_sk VARCHAR,
    quantity INTEGER,
    unit_price DOUBLE,
    total_amount DOUBLE,
    order_date DATE,
    order_year INTEGER,
    order_month INTEGER
);
