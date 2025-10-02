import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

def get_db_connection():
    if DATABASE_URL:
        return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor), 'pg'
    else:
        conn = sqlite3.connect('robo.db')
        conn.row_factory = sqlite3.Row
        return conn, 'sqlite'

def create_admin():
    conn, kind = get_db_connection()
    cur = conn.cursor()

    # Cria tabela users se não existir
    if kind == 'pg':
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    else:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    # Insere usuário admin
    admin_password = generate_password_hash('admin123')
    if kind == 'pg':
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s) ON CONFLICT (username) DO NOTHING",
            ('admin', admin_password)
        )
    else:
        cur.execute(
            "INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)",
            ('admin', admin_password)
        )

    conn.commit()
    conn.close()
    print("✅ Usuário admin/admin123 criado!")

if __name__ == "__main__":
    create_admin()
