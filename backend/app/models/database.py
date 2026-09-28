import sqlite3
from contextlib import contextmanager
from backend.app.core.config import settings
import json
from pathlib import Path


@contextmanager
def get_db():
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(users)
        cursor.execute(products)
        cursor.execute(orders)
        cursor.execute(recipt)
        cursor.execute(logs)
        conn.commit()
        print("Database tables created successfully.")

# * users table 

users = """CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE NOT NULL,
email TEXT UNIQUE NOT NULL,
hashed_password TEXT NOT NULL,
phone TEXT, 
role TEXT DEFAULT 'client',
city TEXT,
auth_provider TEXT DEFAULT 'local',
is_active DEFAULT 1,
created_at TEXT DEFAULT CURRENT_TIMESTAMP
)"""


# ^ products table

products = """CREATE TABLE IF NOT EXISTS products(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
author TEXT Not NULL, 
genre TEXT NOT NULL, 
release_date INTEGER,
rating FLOAT,
price FLOAT NOT NULL, 
stock INTEGER NOT NULL DEFAULT 0,
image TEXT,
description TEXT  
)"""

#& Orders table

orders = """CREATE TABLE IF NOT EXISTS orders(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
total_price FLOAT NOT NULL, 
status TEXT DEFAULT 'pending',
created_at TEXT DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (user_id) REFERENCES users (id)
)"""

#? recipt table (AKA orders_items table)

recipt = """CREATE TABLE IF NOT EXISTS recipt(
id INTEGER PRIMARY KEY AUTOINCREMENT,
order_id INTEGER NOT NULL,
prod_id INTEGER NOT NULL,
quantity INTEGER NOT NULL, 
unit_price REAL NOT NULL,
FOREIGN KEY (order_id) REFERENCES orders (id),
FOREIGN KEY (prod_id) REFERENCES products(id)
)"""

# ! Logs table (AKA telemtry table)

logs = """CREATE TABLE IF NOT EXISTS logs (
id INTEGER PRIMARY KEY AUTOINCREMENT,
ip_add TEXT NOT NULL,
path TEXT NOT NULL, 
method TEXT NOT NULL,
status_code INTEGER NOT NULL, 
timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
user_id INTEGER,
latency_ms REAL NOT NULL
)"""


# * Getting the data from manga.json
def seed_db():
    with get_db() as conn:
        cursor = conn.cursor()
        
        #^ Check if products already exist
        cursor.execute("SELECT COUNT(*) FROM products;")
        count = cursor.fetchone()[0]
    
        # ! HERE when product table is created then it skips it and not make it again !! 
        if count > 0:
            print("Products table already seeded. Skipping.")
            return

        json_path = Path(__file__).resolve().parent.parent / "data" / "manga.json"
        
        if not json_path.exists():
            print(f"Seed file not found at: {json_path}")
            return
            
        #^ Read JSON data
        with open(json_path, "r", encoding="utf-8") as f:
            manga_list = json.load(f)

        insert_sql = """
        INSERT INTO products (title, author, genre, release_date, rating, price, stock, image, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        
        for item in manga_list:
            cursor.execute(insert_sql, (
                item["title"],
                item["author"],
                item["genre"],
                item.get("release_date"),
                item.get("rating"),
                item["price"],
                item["stock"],
                item.get("image"),
                item.get("description")
            ))

        conn.commit()