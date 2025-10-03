import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash

# Lê a variável exatamente como no código do app
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

def get_pg_conn():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def get_sqlite_conn():
    conn = sqlite3.connect('robo.db')
    conn.row_factory = sqlite3.Row
    return conn

def ensure_users_table(cursor, kind='pg'):
    if kind == 'pg':
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    else:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

def reset_admin():
    # decide Postgres (produção) ou SQLite (dev)
    using_pg = bool(DATABASE_URL)
    print("➡️  Banco:", "Postgres (Render)" if using_pg else "SQLite local")

    if using_pg:
        conn = get_pg_conn()
        cur = conn.cursor()
        kind = 'pg'
    else:
        conn = get_sqlite_conn()
        cur = conn.cursor()
        kind = 'sqlite'

    # garante tabela
    ensure_users_table(cur, kind)

    # apaga admin(es) antigos
    if kind == 'pg':
        cur.execute("DELETE FROM users WHERE username IN (%s, %s)", ("admin", "admin@example.com"))
    else:
        cur.execute("DELETE FROM users WHERE username IN (?, ?)", ("admin", "admin@example.com"))

    # cria admin com senha HASH (compatível com check_password_hash)
    hashed = generate_password_hash("admin123")
    if kind == 'pg':
        cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", ("admin", hashed))
    else:
        cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ("admin", hashed))

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Usuário 'admin' recriado com senha 'admin123'.")

if __name__ == "__main__":
    try:
        reset_admin()
    except Exception as e:
        print("❌ Erro ao resetar admin:", e)
        raise
