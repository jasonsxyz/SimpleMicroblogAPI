import sqlite3

DB = 'database.db'

def get_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Users")
        return [dict(row) for row in cursor.fetchall()]
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
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def find_user_from_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def get_post(post_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * From Post WHERE post_id = ?", (post_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def get_comments(post_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * From Comment WHERE post_id = ? ORDER BY created_at DESC", (post_id,))
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()

def get_posts(amount, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        if not user_id:
            cursor.execute("SELECT * FROM Post ORDER BY created_at DESC LIMIT ?", (amount,))
        else:
            cursor.execute("SELECT * FROM Post WHERE user_id = ? ORDER BY created_at DESC LIMIT ?", (user_id, amount,))
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()

def create_post(name, content):
    user = find_user(name)
    if not user:
        create_user(name)
        user = find_user(name)

    user_id = user['user_id']

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO Post (user_id, content) 
        VALUES (?, ?)
        """, (user_id, content))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def create_comment(name, content, post_id):
    user = find_user(name)
    if not user:
        create_user(name)
        user = find_user(name)

    user_id = user['user_id']

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO Comment (post_id, user_id, content) 
        VALUES (?, ?, ?)
        """, (post_id, user_id, content))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()