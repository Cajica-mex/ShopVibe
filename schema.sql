-- TODO: Define dim_products: id (INTEGER PRIMARY KEY), product_name (TEXT NOT NULL), price (REAL NOT NULL), category (TEXT)
CREATE TABLE dim_products (
    id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    price REAL NOT NULL,
    category TEXT
);

-- TODO: Define  dim_customers: id (INTEGER PRIMARY KEY), customer_name (TEXT NOT NULL), email (TEXT NOT NULL)
CREATE TABLE dim_customers (
    id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    email TEXT NOT NULL
);

-- TODO: fact_sales: id (INTEGER PRIMARY KEY), customer_id (INTEGER, FK a dim_customers), product_id (INTEGER, FK a dim_products), quantity (INTEGER), sale_date (TEXT), total_amount (REAL)
CREATE TABLE fact_sales (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    sale_date TEXT,
    total_amount REAL,
    FOREIGN KEY (customer_id) REFERENCES dim_customers(id),
    FOREIGN KEY (product_id) REFERENCES dim_products(id)
);
