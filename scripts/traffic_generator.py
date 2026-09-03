# traffic_generator.py
import os
import json
import csv
import random
import argparse
from datetime import datetime, timedelta

def generate_data(output_dir, inject_email, inject_amount, inject_duplicates, inject_delimiters):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Generate products catalog (CSV)
    products_file = os.path.join(output_dir, 'products.csv')
    products = [
        {"id": 1, "product_name": "Remera de Algodón, Classic Blue", "price": 25.99, "category": "Ropa"},
        {"id": 2, "product_name": "Jeans Slim Fit", "price": 59.99, "category": "Ropa"},
        {"id": 3, "product_name": "Zapatillas Urbanas", "price": 89.99, "category": "Calzado"},
        {"id": 4, "product_name": "Buzo Oversize con Capucha", "price": 45.50, "category": "Ropa"},
        {"id": 5, "product_name": "Gorra de Gabardina", "price": 19.99, "category": "Accesorios"}
    ]
    
    with open(products_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "product_name", "price", "category"])
        for p in products:
            pname = p["product_name"]
            # Inject delimiter anomalies: unescaped commas inside the text field
            if inject_delimiters and p["id"] == 1:
                # E.g. write it raw without wrapping quotes in csv
                f.write(f"{p['id']},{pname},{p['price']},{p['category']}\n")
            else:
                writer.writerow([p["id"], pname, p["price"], p["category"]])
                
    # 2. Generate daily sales orders (JSON)
    sales_file = os.path.join(output_dir, 'sales_orders.json')
    orders = []
    
    customers = [
        {"id": 10, "customer_name": "Juan Perez", "email": "juan.perez@example.com"},
        {"id": 11, "customer_name": "Maria Rodriguez", "email": "maria.rodriguez@example.com"},
        {"id": 12, "customer_name": "Carlos Gomez", "email": "carlos.gomez@example.com"},
        {"id": 13, "customer_name": "Ana Lopez", "email": "ana.lopez@example.com"}
    ]
    
    base_date = datetime.now() - timedelta(days=5)
    
    for i in range(1, 21):
        order_id = 1000 + i
        cust = random.choice(customers)
        cust_email = cust["email"]
        
        # Inject invalid email anomalies
        if inject_email and i % 7 == 0:
            cust_email = "invalid_email_no_at"
            
        prod = random.choice(products)
        qty = random.randint(1, 3)
        monto = prod["price"] * qty
        
        # Inject negative/zero amount anomalies
        if inject_amount and i % 8 == 0:
            monto = -monto if i % 2 == 0 else 0.0
            
        order_date = (base_date + timedelta(hours=i * 4)).strftime("%Y-%m-%d")
        
        # Inconsistent separators for dates in JSON logs
        if i % 5 == 0:
            order_date = (base_date + timedelta(hours=i * 4)).strftime("%Y.%m.%d")
        elif i % 6 == 0:
            order_date = (base_date + timedelta(hours=i * 4)).strftime("%Y/%m/%d")
            
        ord_obj = {
            "id": order_id,
            "cliente_id": cust["id"],
            "cliente_name": cust["customer_name"],
            "email": cust_email,
            "fecha": order_date,
            "articulos": [
                {
                    "producto_id": prod["id"],
                    "cantidad": qty,
                    "precio": prod["price"]
                }
            ]
        }
        orders.append(ord_obj)
        
    # 3. Generate customers catalog (CSV)
    customers_file = os.path.join(output_dir, 'customers.csv')
    with open(customers_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "customer_name", "email", "address", "signup_date"])
        states = ["123 Main St, New York, NY 10001", "456 Market St, Los Angeles, CA 90001", "789 Elm St, Chicago, IL 60601", "321 Oak St, Houston, TX 77001"]
        for idx, c in enumerate(customers):
            c_email = c["email"]
            if inject_email and idx == 0:
                c_email = "invalid_email_no_at"
            addr = states[idx % len(states)]
            signup = (base_date - timedelta(days=idx * 10)).strftime("%Y-%m-%d")
            writer.writerow([c["id"], c["customer_name"], c_email, addr, signup])

    print(f"Data generation complete. Outputs saved in {output_dir}")
    print(f"Products: {products_file}")
    print(f"Orders: {sales_file}")
    print(f"Customers: {customers_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ShopVibe Purchase Traffic Generator")
    parser.add_argument('--output-dir', type=str, default='data/raw', help='Directory to output raw logs')
    parser.add_argument('--anomalies-email', action='store_true', help='Inject invalid email anomalies')
    parser.add_argument('--anomalies-amount', action='store_true', help='Inject negative/zero amount anomalies')
    parser.add_argument('--anomalies-duplicates', action='store_true', help='Inject duplicate order anomalies')
    parser.add_argument('--anomalies-delimiters', action='store_true', help='Inject malformed CSV delimiter anomalies')
    parser.add_argument('--anomalies-all', action='store_true', help='Inject all types of anomalies')
    
    args = parser.parse_args()
    
    if args.anomalies_all:
        args.anomalies_email = True
        args.anomalies_amount = True
        args.anomalies_duplicates = True
        args.anomalies_delimiters = True
        
    generate_data(
        args.output_dir,
        args.anomalies_email,
        args.anomalies_amount,
        args.anomalies_duplicates,
        args.anomalies_delimiters
    )
