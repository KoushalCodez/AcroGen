import sqlite3
import random
from datetime import datetime, timedelta

PRODUCTS = ["Widget A", "Widget B", "Super Gizmo", "Mega Dongle", "Hyper Connector", "Ultra Cable"]
CUSTOMERS = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy"]

def seed_db():
    # Connect to SQLite database (this will create it if it doesn't exist)
    conn = sqlite3.connect('report.db')
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT,
            product TEXT,
            amount REAL,
            created_at DATE
        )
    ''')

    # Delete all existing rows so the script is safe to run multiple times
    cursor.execute('DELETE FROM orders')
    
    # Generate ~200 random orders
    num_orders = 200
    now = datetime.now()
    
    orders = []
    for _ in range(num_orders):
        customer = random.choice(CUSTOMERS)
        product = random.choice(PRODUCTS)
        # Random amount between 5 and 200
        amount = round(random.uniform(5.0, 200.0), 2)
        
        # Random date in the last 30 days
        random_days = random.randint(0, 30)
        random_seconds = random.randint(0, 24 * 3600 - 1)
        created_at = (now - timedelta(days=random_days, seconds=random_seconds)).strftime("%Y-%m-%d %H:%M:%S")
        
        orders.append((customer, product, amount, created_at))
        
    # Insert the records
    cursor.executemany('''
        INSERT INTO orders (customer, product, amount, created_at)
        VALUES (?, ?, ?, ?)
    ''', orders)
    
    # Commit the changes and close the connection
    conn.commit()
    print(f"Successfully seeded {cursor.rowcount} orders into report.db")
    conn.close()

if __name__ == "__main__":
    seed_db()
