# backend/student_model.py

from backend.db_connection import get_connection

def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name FROM students")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return students
