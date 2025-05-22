# frontend/students/student_profile_window.py

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton
)
from PyQt5.QtCore import Qt
from frontend import style
from backend.db_connection import get_connection

class StudentProfileWindow(QWidget):
    def __init__(self, student_id):
        super().__init__()
        self.student_id = student_id
        self.setWindowTitle("Profil Élève")
        self.setGeometry(350, 250, 400, 400)
        self.setup_ui()
        self.load_student_profile()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        self.title_label = QLabel("Profil de l'élève")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(style.TITLE_STYLE)

        self.name_label = QLabel()
        self.birth_date_label = QLabel()
        self.phone_label = QLabel()
        self.address_label = QLabel()
        self.class_label = QLabel()

        # Retour bouton
        self.back_button = QPushButton("🔙 Retour")
        self.back_button.setStyleSheet(style.BUTTON_STYLE)
        self.back_button.clicked.connect(self.close)

        # Ajouter tous les éléments au layout
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.birth_date_label)
        self.layout.addWidget(self.phone_label)
        self.layout.addWidget(self.address_label)
        self.layout.addWidget(self.class_label)
        self.layout.addStretch()
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    def load_student_profile(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT full_name, birth_date, phone_number, address, student_class
                FROM students
                WHERE id = %s
            """, (self.student_id,))
            student = cursor.fetchone()
            cursor.close()
            conn.close()

            if student:
                self.name_label.setText(f"👤 Nom : {student[0]}")
                self.birth_date_label.setText(f"📅 Date de naissance : {student[1]}")
                self.phone_label.setText(f"📞 Téléphone : {student[2]}")
                self.address_label.setText(f"🏠 Adresse : {student[3]}")
                self.class_label.setText(f"🎓 Classe : {student[4]}")

        except Exception as e:
            self.name_label.setText(f"Erreur : {str(e)}")
