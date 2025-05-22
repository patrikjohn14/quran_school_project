# frontend/courses/course_students_window.py

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QListWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from frontend import style
from backend import course_model
from backend.db_connection import get_connection

class CourseStudentsWindow(QWidget):
    def __init__(self, course_id):
        super().__init__()
        self.course_id = course_id
        self.setWindowTitle("Élèves associés au Cours")
        self.setGeometry(350, 250, 500, 500)
        self.setup_ui()
        self.load_students()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        self.title_label = QLabel("Liste des élèves du cours")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(style.TITLE_STYLE)

        self.students_list = QListWidget()
        self.students_list.setStyleSheet(style.INPUT_STYLE)

        self.back_button = QPushButton("🔙 Retour")
        self.back_button.setStyleSheet(style.BUTTON_STYLE)
        self.back_button.clicked.connect(self.close)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.students_list)
        self.layout.addStretch()
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    def load_students(self):
        try:
            course = course_model.get_course_by_id(self.course_id)
            if not course:
                QMessageBox.warning(self, "Erreur", "Cours non trouvé.")
                return

            class_name = course[3]  # Le champ class_name du cours

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT full_name, phone_number
                FROM students
                WHERE student_class = %s
            """, (class_name,))
            students = cursor.fetchall()
            cursor.close()
            conn.close()

            if students:
                for student in students:
                    self.students_list.addItem(f"{student[0]} - {student[1]}")
            else:
                self.students_list.addItem("Aucun élève trouvé pour cette classe.")

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement : {str(e)}")
