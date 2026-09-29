import difflib
from typing import Optional
from backend.app.models.database import get_db
# ^ Here it is the model of product file that fetch what user asked from the DB 
def get_products(genre: Optional[str] = None, search: Optional[str] = None):
    with get_db() as conn:
        cursor = conn.cursor()

        genre = genre.strip() if genre else None 
        search = search.strip() if search else None 

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

    
        if rows:
            return [dict(r) for r in rows]

        # TODO Fuzzy Search Fallback (Runs if SQL found 0 results for genre OR search)
        if genre or search:
            cursor.execute("SELECT * FROM products")
            all_products = cursor.fetchall()
            fuzzy_results = []

            for row in all_products:
                prod = dict(row)

                #! Evaluate genre fuzzy 
                genre_match = True
                if genre:
                    genre_words = prod['genre'].lower().replace(',', ' ').split()
                    genre_match = bool(difflib.get_close_matches(genre.lower(), genre_words, cutoff=0.6))

                #? Evaluate search fuzzy 
                search_match = True
                if search:
                    search_words = f"{prod['title']} {prod['author']}".lower().split()
                    search_match = bool(difflib.get_close_matches(search.lower(), search_words, cutoff=0.6))

                if genre_match and search_match:
                    fuzzy_results.append(prod)
            return fuzzy_results
        return []
    
def getProductById(product_id: int):
    with get_db() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()

        result_id = dict(row) if row else None
        return result_id