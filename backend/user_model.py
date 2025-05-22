# backend/user_model.py

from backend.db_connection import get_connection

def register_user(username, password, role='teacher'):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    INSERT INTO users (username, password, role)
    VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (username, password, role))
    conn.commit()
    cursor.close()
    conn.close()

def verify_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT id, role FROM users WHERE username = %s AND password = %s"
    cursor.execute(sql, (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user
