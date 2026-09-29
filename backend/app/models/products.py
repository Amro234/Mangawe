from typing import Optional
from backend.app.models.database import get_db
# ^ Here it is the model of product file that fetch what user asked from the DB 
def get_products(genre: Optional[str] = None, search: Optional[str] = None):
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM products WHERE 1=1"
        params = []

        if genre: 
            query += " AND genre LIKE ?"
            params.append(f"%{genre}%")

        if search:
            query += " AND (title LIKE ? OR author LIKE ?)"
            params.append(f"%{search}%")
            params.append(f"%{search}%")


        cursor.execute(query, params)
        rows = cursor.fetchall()

        result_search = [dict(row) for row in rows]  
        return result_search


def getProductById(product_id: int):
    with get_db() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()

        result_id = dict(row) if row else None
        return result_id

    