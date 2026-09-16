import os
import sqlite3

data_directory =  os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
db_dir = os.path.join(data_directory, "mangawe_DB.db")
os.makedirs(data_directory, exist_ok=True)

db = sqlite3.connect(db_dir)

cursor = db.cursor()

# * users table 

users = """CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE NOT NULL,
email TEXT UNIQUE NOT NULL,
hashed_password TEXT NOT NULL,
phone TEXT, 
role TEXT DEFAULT 'client',
city TEXT,
is_active BOOLEAN DEFAULT 1,
created_at TEXT DEFAULT CURRENT_TIMESTAMP
)"""

cursor.execute(users)

# ^ products table

products = """CREATE TABLE IF NOT EXISTS products(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
author TEXT Not NULL, 
genre TEXT NOT NULL, 
release_dte INTEGER,
rating FLOAT,
price FLOAT NOT NULL, 
stock INTEGER NOT NULL DEFAULT 0,
image TEXT,
description TEXT  
)"""

cursor.execute(products)


#& Orders table

orders = """CREATE TABLE IF NOT EXISTS orders(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
quantity INTEGER DEFAULT 1,
total_price FLOAT NOT NULL, 
status TEXT DEFAULT 'pending',
created_at TEXT DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (user_id) REFERENCES users (id)
)"""

cursor.execute(orders) 

#? recipt table (AKA orders_items table)

recipt = """CREATE TABLE IF NOT EXISTS recipt(
id INTEGER PRIMARY KEY AUTOINCREMENT,
order_id INTEGER NOT NULL,
prod_id INTEGER NOT NULL,
quntety INTEGER NOT NULL, 
full_price INTEGER NOT NULL,
FOREIGN KEY (order_id) REFERENCES orders (id),
FOREIGN KEY (prod_id) REFERENCES products(id)
)"""

cursor.execute(recipt)

# ! Logs table (AKA telemtry table)

logs = """CREATE TABLE IF NOT EXISTS logs (
id INTEGER PRIMARY KEY AUTOINCREMENT,
ip INTEGER NOT NULL,
path TEXT NOT NULL, 
method TEXT NOT NULL,
status_code INTEGER NOT NULL, 
timestamp TEXT DEFUALT CURRENT_TIMESTAMP
)"""

cursor.execute(logs)

db.commit()
db.close()





