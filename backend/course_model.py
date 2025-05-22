# backend/course_model.py

from backend.db_connection import get_connection

def add_course(data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    INSERT INTO courses (course_name, description, class_name, teacher_id)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, data)
    conn.commit()
    cursor.close()
    conn.close()

def get_all_courses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT courses.id, courses.course_name, courses.description, courses.class_name, teachers.full_name
        FROM courses
        LEFT JOIN teachers ON courses.teacher_id = teachers.id
    """)
    courses = cursor.fetchall()
    cursor.close()
    conn.close()
    return courses

def get_course_by_id(course_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses WHERE id = %s", (course_id,))
    course = cursor.fetchone()
    cursor.close()
    conn.close()
    return course

def update_course(course_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    UPDATE courses
    SET course_name = %s, description = %s, class_name = %s, teacher_id = %s
    WHERE id = %s
    """
    cursor.execute(sql, data + (course_id,))
    conn.commit()
    cursor.close()
    conn.close()

def delete_course(course_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM courses WHERE id = %s", (course_id,))
    conn.commit()
    cursor.close()
    conn.close()
