# init_db.py

import sqlite3

# Connexion (crée rss.db si absent)
conn = sqlite3.connect("rss.db")
cursor = conn.cursor()

# Création de la table "articles"
cursor.execute("""
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    link TEXT UNIQUE,
    publication TEXT,
    published TEXT,
    stored_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Base de données 'rss.db' créée avec la table 'articles'.")
