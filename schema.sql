-- schema.sql
-- DDL para el Star Schema analítico de ShopVibe (SQLite)

-- TODO 1: Crear la tabla dim_products
-- Columnas: id (INTEGER PRIMARY KEY), product_name (TEXT NOT NULL), price (REAL NOT NULL), category (TEXT)


-- TODO 2: Crear la tabla dim_customers
-- Columnas: id (INTEGER PRIMARY KEY), customer_name (TEXT NOT NULL), email (TEXT NOT NULL)


-- TODO 3: Crear la tabla fact_sales
-- Columnas: id (INTEGER PRIMARY KEY), customer_id (INTEGER), product_id (INTEGER), quantity (INTEGER NOT NULL), sale_date (TEXT NOT NULL), total_amount (REAL NOT NULL)
-- Claves foráneas:
--   customer_id referenciando a dim_customers(id)
--   product_id referenciando a dim_products(id)
