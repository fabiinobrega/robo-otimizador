"""
DB Utils - Módulo utilitário centralizado para conexão com banco de dados
=========================================================================

Este módulo fornece funções utilitárias para conexão com banco de dados,
suportando tanto SQLite (desenvolvimento local) quanto PostgreSQL (produção).

Autor: MANUS AI
Data: 03/02/2026
"""

import os
import sqlite3
from typing import Any, Optional

# Tentar importar psycopg2 para PostgreSQL
try:
    import psycopg2
    import psycopg2.extras
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    print("Warning: psycopg2 not available, using SQLite only")

# Configurações
DATABASE_PATH = os.environ.get('DATABASE_PATH', 'database.db')
DATABASE_URL = os.environ.get('DATABASE_URL', '')
USE_POSTGRES = bool(DATABASE_URL) and POSTGRES_AVAILABLE

print(f"🔧 DB Utils: USE_POSTGRES={USE_POSTGRES}, POSTGRES_AVAILABLE={POSTGRES_AVAILABLE}")


def get_db_connection():
    """
    Retorna conexão com PostgreSQL ou SQLite.
    
    Returns:
        Conexão com o banco de dados
    """
    if USE_POSTGRES:
        return psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
    return sqlite3.connect(DATABASE_PATH)


def sql_param(query: str) -> str:
    """
    Converte placeholders ? para %s quando usando PostgreSQL.
    
    Args:
        query: Query SQL com placeholders ?
        
    Returns:
        Query SQL com placeholders corretos para o banco atual
    """
    if USE_POSTGRES:
        return query.replace('?', '%s')
    return query


def dict_factory(cursor, row):
    """
    Factory para converter rows SQLite em dicionários.
    
    Args:
        cursor: Cursor SQLite
        row: Row SQLite
        
    Returns:
        Dicionário com os dados da row
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db_connection_with_dict():
    """
    Retorna conexão com banco de dados configurada para retornar dicionários.
    
    Returns:
        Conexão com o banco de dados
    """
    if USE_POSTGRES:
        return psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
    else:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = dict_factory
        return conn


def execute_query(query: str, params: tuple = (), fetch: str = 'all') -> Any:
    """
    Executa uma query SQL e retorna os resultados.
    
    Args:
        query: Query SQL com placeholders ?
        params: Parâmetros para a query
        fetch: 'all' para fetchall, 'one' para fetchone, 'none' para executar sem retorno
        
    Returns:
        Resultados da query
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql_param(query), params)
        
        if fetch == 'all':
            result = cursor.fetchall()
        elif fetch == 'one':
            result = cursor.fetchone()
        else:
            result = None
            conn.commit()
        
        return result
    finally:
        conn.close()


def execute_insert(query: str, params: tuple = ()) -> int:
    """
    Executa um INSERT e retorna o ID gerado.
    
    Args:
        query: Query SQL de INSERT com placeholders ?
        params: Parâmetros para a query
        
    Returns:
        ID do registro inserido
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql_param(query), params)
        
        if USE_POSTGRES:
            cursor.execute("SELECT lastval()")
            result = cursor.fetchone()
            insert_id = result[0] if isinstance(result, tuple) else result.get('lastval', 0)
        else:
            insert_id = cursor.lastrowid
        
        conn.commit()
        return insert_id
    finally:
        conn.close()


def is_postgres() -> bool:
    """
    Verifica se está usando PostgreSQL.
    
    Returns:
        True se estiver usando PostgreSQL, False caso contrário
    """
    return USE_POSTGRES
