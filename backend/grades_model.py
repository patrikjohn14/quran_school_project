# backend/grades_model.py

from backend.db_connection import get_connection

def add_grade(student_id, course_id, grade):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    INSERT INTO grades (student_id, course_id, grade)
    VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (student_id, course_id, grade))
    conn.commit()
    cursor.close()
    conn.close()

def get_grades():
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    SELECT students.full_name, courses.course_name, grades.grade
    FROM grades
    JOIN students ON grades.student_id = students.id
    JOIN courses ON grades.course_id = courses.id
    """
    cursor.execute(sql)
    grades = cursor.fetchall()
    cursor.close()
    conn.close()
    return grades

def get_all_grades_with_ids():
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    SELECT grades.id, students.full_name, courses.course_name, grades.grade
    FROM grades
    JOIN students ON grades.student_id = students.id
    JOIN courses ON grades.course_id = courses.id
    """
    cursor.execute(sql)
    grades = cursor.fetchall()
    cursor.close()
    conn.close()
    return grades

def update_grade(grade_id, new_grade):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "UPDATE grades SET grade = %s WHERE id = %s"
    cursor.execute(sql, (new_grade, grade_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_grade(grade_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM grades WHERE id = %s"
    cursor.execute(sql, (grade_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_average_grade():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(grade) FROM grades")
    avg = cursor.fetchone()[0] or 0
    cursor.close()
    conn.close()
    return avg
