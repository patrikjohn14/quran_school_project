# backend/export_model.py

from backend.db_connection import get_connection
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import datetime

def export_attendance_to_pdf():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT students.full_name, courses.course_name, attendance.status
            FROM attendance
            JOIN students ON attendance.student_id = students.id
            JOIN courses ON attendance.course_id = courses.id
        """)
        records = cursor.fetchall()
        cursor.close()
        conn.close()

        c = canvas.Canvas("attendance_report.pdf", pagesize=A4)
        width, height = A4

        # En-tête officiel
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width / 2, height - 2*cm, "École de Qur'an - Rapport de Présences")

        # Date de génération
        c.setFont("Helvetica", 12)
        today = datetime.today().strftime('%d/%m/%Y')
        c.drawString(2*cm, height - 3*cm, f"Date de génération : {today}")

        # Titre de section
        y = height - 5*cm
        c.setFont("Helvetica-Bold", 14)
        c.drawString(2*cm, y, "Liste des présences :")

        y -= 1*cm
        c.setFont("Helvetica", 12)

        for record in records:
            line = f"Élève : {record[0]} | Cours : {record[1]} | Statut : {record[2]}"
            c.drawString(2*cm, y, line)
            y -= 0.8*cm
            if y < 2*cm:
                c.showPage()
                y = height - 2*cm

        c.save()
        return True
    except Exception as e:
        print(e)
        return False

def export_grades_to_pdf():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT students.full_name, courses.course_name, grades.grade
            FROM grades
            JOIN students ON grades.student_id = students.id
            JOIN courses ON grades.course_id = courses.id
        """)
        records = cursor.fetchall()
        cursor.close()
        conn.close()

        c = canvas.Canvas("grades_report.pdf", pagesize=A4)
        width, height = A4

        # En-tête officiel
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width / 2, height - 2*cm, "École de Qur'an - Rapport des Notes")

        # Date de génération
        c.setFont("Helvetica", 12)
        today = datetime.today().strftime('%d/%m/%Y')
        c.drawString(2*cm, height - 3*cm, f"Date de génération : {today}")

        # Titre de section
        y = height - 5*cm
        c.setFont("Helvetica-Bold", 14)
        c.drawString(2*cm, y, "Liste des notes :")

        y -= 1*cm
        c.setFont("Helvetica", 12)

        for record in records:
            line = f"Élève : {record[0]} | Cours : {record[1]} | Note : {record[2]} /20"
            c.drawString(2*cm, y, line)
            y -= 0.8*cm
            if y < 2*cm:
                c.showPage()
                y = height - 2*cm

        c.save()
        return True
    except Exception as e:
        print(e)
        return False
