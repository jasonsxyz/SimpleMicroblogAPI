import sqlite3

DB = 'database.db'

def get_connection():
    conn = sqlite3.connect(DB)
    return conn

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Users",)
        return cursor.fetchall()
    finally:
        conn.close()

def create_user(name):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO Users (username) VALUES (?)", (name,))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def find_user(name):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Users WHERE username = ?", (name,))
        return cursor.fetchone()
    finally:
        conn.close()

def find_user_from_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,))
        return cursor.fetchone()
    finally:
        conn.close()

def get_posts(amount, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    if not user_id:
        try:
            cursor.execute("SELECT * FROM Post ORDER BY created_at DESC LIMIT (?)", (amount,))
            return cursor.fetchall()
        finally:
            conn.close()
    else:
        try:
            cursor.execute("SELECT * FROM Post WHERE user_id = ? ORDER BY created_at DESC LIMIT ?", (user_id, amount,))
            return cursor.fetchall()
        finally:
            conn.close()

def create_post(name, content):
    conn = get_connection()
    cursor = conn.cursor()
    user_id = find_user(name)[0]

    try:
        cursor.execute("""
        INSERT INTO Post (user_id, content) 
        VALUES (?, ?)
        """, (user_id, content))
        conn.commit()
        return cursor.fetchone()
    finally:
        conn.close()

