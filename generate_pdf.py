import os
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright
from report import getReportData

def build_html(data):
    today = datetime.now().strftime("%B %d, %Y")
    
    # CSS to fix page breaks and style the report
    css = """
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; color: #333; }
        h1 { color: #2c3e50; }
        .totals { display: flex; gap: 40px; margin-bottom: 30px; font-size: 1.2em; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 30px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #f8f9fa; font-weight: bold; }
        
        /* The classic trap fix: prevent slicing rows in half across pages */
        tr { break-inside: avoid; }
        
        /* Repeat header on every page */
        thead { display: table-header-group; }
    </style>
    """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Shop Report - {today}</title>
        {css}
    </head>
    <body>
        <h1>Little Shop Report - {today}</h1>
        
        <div class="totals">
            <div><strong>Total Orders:</strong> {data['total_orders']}</div>
            <div><strong>Total Revenue:</strong> ${data['total_revenue']:.2f}</div>
        </div>
        
        <h2>Top 5 Products</h2>
        <table>
            <thead>
                <tr>
                    <th>Product</th>
                    <th>Revenue</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for p in data['top_products']:
        html += f"""
                <tr>
                    <td>{p['product']}</td>
                    <td>${p['revenue']:.2f}</td>
                </tr>
        """
        
    html += """
            </tbody>
        </table>
        
        <h2>All Orders</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Customer</th>
                    <th>Product</th>
                    <th>Amount</th>
                    <th>Date</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for o in data['all_orders']:
        html += f"""
                <tr>
                    <td>{o['id']}</td>
                    <td>{o['customer']}</td>
                    <td>{o['product']}</td>
                    <td>${o['amount']:.2f}</td>
                    <td>{o['created_at']}</td>
                </tr>
        """
        
    html += """
            </tbody>
        </table>
    </body>
    </html>
    """
    
    return html

async def generate_pdf(pdf_path="reports/test.pdf"):
    # Ensure reports directory exists
    os.makedirs("reports", exist_ok=True)
    
    data = getReportData()
    html_content = build_html(data)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        await page.set_content(html_content, wait_until="networkidle")
        
        await page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True
        )
        
        print(f"Report saved to {pdf_path}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(generate_pdf())
