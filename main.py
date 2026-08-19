import os
import sqlite3
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from generate_pdf import generate_pdf

app = FastAPI()

def init_db():
    conn = sqlite3.connect('report.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT,
            created_at DATE
        )
    ''')
    conn.commit()
    conn.close()

# Run DB initialization on load
init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/reports", status_code=201)
async def create_report():
    conn = sqlite3.connect('report.db')
    cursor = conn.cursor()
    
    # Insert an initial record to generate an ID
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO reports (path, created_at) VALUES (?, ?)", ("", now))
    report_id = cursor.lastrowid
    
    pdf_path = f"reports/{report_id}.pdf"
    
    # Update the row with the actual PDF path
    cursor.execute("UPDATE reports SET path = ? WHERE id = ?", (pdf_path, report_id))
    conn.commit()
    conn.close()
    
    # Run the PDF generation pipeline (this will hang for a few seconds)
    await generate_pdf(pdf_path)
    
    return {"id": report_id, "file": f"/reports/{report_id}/file"}

@app.get("/reports/{report_id}")
def get_report(report_id: int):
    conn = sqlite3.connect('report.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, path, created_at FROM reports WHERE id = ?", (report_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Report not found")
        
    return {
        "id": row['id'],
        "path": row['path'],
        "created_at": row['created_at'],
        "file": f"/reports/{report_id}/file"
    }

@app.get("/reports/{report_id}/file")
def get_report_file(report_id: int):
    conn = sqlite3.connect('report.db')
    cursor = conn.cursor()
    cursor.execute("SELECT path FROM reports WHERE id = ?", (report_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row or not os.path.exists(row[0]):
        raise HTTPException(status_code=404, detail="Report file not found")
        
    return FileResponse(row[0], media_type="application/pdf", filename=f"report_{report_id}.pdf")
