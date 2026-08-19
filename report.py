import sqlite3
import json
from datetime import datetime, timedelta

def getReportData():
    conn = sqlite3.connect('report.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 1. Total number of orders
    cursor.execute("SELECT COUNT(*) as total_orders FROM orders")
    total_orders = cursor.fetchone()['total_orders']
    
    # 2. Total revenue (SUM(amount))
    cursor.execute("SELECT SUM(amount) as total_revenue FROM orders")
    total_revenue_row = cursor.fetchone()
    total_revenue = total_revenue_row['total_revenue'] if total_revenue_row['total_revenue'] is not None else 0.0
    
    # 3. Top 5 products by revenue (GROUP BY product ORDER BY ... LIMIT 5)
    cursor.execute("""
        SELECT product, SUM(amount) as revenue 
        FROM orders 
        GROUP BY product 
        ORDER BY revenue DESC 
        LIMIT 5
    """)
    top_products = [{"product": row['product'], "revenue": round(row['revenue'], 2)} for row in cursor.fetchall()]
    
    # 4. Orders per day for the last 7 days
    # Using python's datetime to avoid UTC vs local timezone mismatches with SQLite's 'now'
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    cursor.execute("""
        SELECT DATE(created_at) as order_date, COUNT(*) as order_count 
        FROM orders 
        WHERE DATE(created_at) >= ?
        GROUP BY order_date
        ORDER BY order_date DESC
    """, (seven_days_ago,))
    orders_per_day = [{"date": row['order_date'], "count": row['order_count']} for row in cursor.fetchall()]
    
    # 5. All orders for the long table
    cursor.execute("""
        SELECT id, customer, product, amount, created_at
        FROM orders
        ORDER BY created_at DESC
    """)
    all_orders = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return {
        "total_orders": total_orders,
        "total_revenue": round(total_revenue, 2),
        "top_products": top_products,
        "orders_per_day_last_7_days": orders_per_day,
        "all_orders": all_orders
    }

if __name__ == "__main__":
    report_data = getReportData()
    print(json.dumps(report_data, indent=2))
