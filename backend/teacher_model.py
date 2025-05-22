# backend/teacher_model.py

from backend.db_connection import get_connection

def add_teacher(data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    INSERT INTO teachers (full_name, gender, specialization, phone_number, email, address, hire_date, diploma, years_experience, notes)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, data)
    conn.commit()
    cursor.close()
    conn.close()

def get_all_teachers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teachers")
    teachers = cursor.fetchall()
    cursor.close()
    conn.close()
    return teachers

def get_teacher_by_id(teacher_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teachers WHERE id = %s", (teacher_id,))
    teacher = cursor.fetchone()
    cursor.close()
    conn.close()
    return teacher

def update_teacher(teacher_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    UPDATE teachers
    SET full_name = %s, gender = %s, specialization = %s, phone_number = %s, email = %s,
        address = %s, hire_date = %s, diploma = %s, years_experience = %s, notes = %s
    WHERE id = %s
    """
    cursor.execute(sql, data + (teacher_id,))
    conn.commit()
    cursor.close()
    conn.close()

def delete_teacher(teacher_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM teachers WHERE id = %s", (teacher_id,))
    conn.commit()
    cursor.close()
    conn.close()
