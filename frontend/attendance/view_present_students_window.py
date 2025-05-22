# frontend/attendance/view_present_students_window.py

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QListWidget, QMessageBox
from PyQt5.QtCore import Qt
from frontend import style
from backend.attendance_model import get_present_students

class ViewPresentStudentsWindow(QWidget):
    def __init__(self, course_id, date):
        super().__init__()
        self.course_id = course_id
        self.date = date
        self.setWindowTitle("Élèves Présents")
        self.setGeometry(350, 250, 500, 400)
        self.setup_ui()
        self.load_present_students()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        self.title_label = QLabel(f"Liste des élèves présents pour le cours à la date {self.date}")
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

    def load_present_students(self):
        try:
            present_students = get_present_students(self.course_id, self.date)
            if present_students:
                for student in present_students:
                    self.students_list.addItem(f"{student[0]} - {student[1]}")
            else:
                self.students_list.addItem("Aucun élève n'est présent.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement : {str(e)}")
