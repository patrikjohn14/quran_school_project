# backend/attendance_model.py

from backend.db_connection import get_connection

# Ajouter une présence pour un élève, un cours, une date et un statut
def add_attendance(student_id, course_id, date, status):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    INSERT INTO attendance (student_id, course_id, date, status)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (student_id, course_id, date, status))
    conn.commit()
    cursor.close()
    conn.close()

# Récupérer toutes les présences pour un cours et une date
def get_attendance(course_id, date):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    SELECT student_id, status
    FROM attendance
    WHERE course_id = %s AND date = %s
    """
    cursor.execute(sql, (course_id, date))
    attendance = cursor.fetchall()
    cursor.close()
    conn.close()
    return attendance

# Récupérer les élèves marqués comme "Présents" pour un cours et une date donnée
def get_present_students(course_id, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT students.full_name, students.phone_number
        FROM attendance
        JOIN students ON attendance.student_id = students.id
        WHERE attendance.course_id = %s AND attendance.date = %s AND attendance.status = 'present'
    """, (course_id, date))
    present_students = cursor.fetchall()
    cursor.close()
    conn.close()
    return present_students


def get_total_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total

def get_total_courses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM courses")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total

def get_total_attendance_records():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM attendance")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total
