from typing import Optional
from backend.app.models.database import get_db
# ^ Here it is the model of product file that fetch what user asked from the DB 
def get_products(genre: Optional[str] = None, search: Optional[str] = None):
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM products WHERE 1=1"
        conditions = []
        params = []

        if genre: 
            conditions.append("genre LIKE ?")
            params.append(f"%{genre}%")

        if search:
            conditions.append("title LIKE ?")
            params.append(f"%{search}%")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        return rows


def getProductById(product_id: int):
    with get_db() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()

        return row