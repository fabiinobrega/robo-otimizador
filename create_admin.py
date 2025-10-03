import os
import psycopg2
import sqlite3
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash

# Verificar qual banco está sendo usado
print("🔎 DATABASE_URL =", os.getenv("DATABASE_URL"))

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

def get_db_connection():
    if DATABASE_URL:
        print("➡️ Conectando ao PostgreSQL...")
        return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    else:
        print("⚠️ Sem DATABASE_URL, caindo no SQLite local...")
        conn = sqlite3.connect("robo.db")
        conn.row_factory = sqlite3.Row
        return conn

def create_admin():
    conn = get_db_connection()
    cur = conn.cursor()

    # Criar tabela se não existir
    if DATABASE_URL:
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

    # Verificar se já existe admin
    cur.execute("SELECT * FROM users WHERE username = %s" if DATABASE_URL else "SELECT * FROM users WHERE username = ?", ("admin",))
    user = cur.fetchone()

    if not user:
        hashed_pw = generate_password_hash("admin123")
        if DATABASE_URL:
            cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", ("admin", hashed_pw))
        else:
            cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ("admin", hashed_pw))
        conn.commit()
        print("✅ Usuário admin/admin123 criado com sucesso!")
    else:
        print("ℹ️ Usuário admin já existe.")

    conn.close()

if __name__ == "__main__":
    create_admin()
