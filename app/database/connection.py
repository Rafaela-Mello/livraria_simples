import mysql.connector
from mysql.connector import Error

from app.config import DB_CONFIG


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def fetch_all(query, params=None):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        conn.close()


def fetch_one(query, params=None):
    rows = fetch_all(query, params)
    return rows[0] if rows else None


def execute(query, params=None):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return cursor.lastrowid
    except Error:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def execute_many(queries_with_params):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        for query, params in queries_with_params:
            cursor.execute(query, params)
        conn.commit()
    except Error:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
