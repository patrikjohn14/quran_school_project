# frontend/teachers/teacher_profile_window.py

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton
)
from PyQt5.QtCore import Qt
from frontend import style
from backend import teacher_model

class TeacherProfileWindow(QWidget):
    def __init__(self, teacher_id):
        super().__init__()
        self.teacher_id = teacher_id
        self.setWindowTitle("Profil Enseignant")
        self.setGeometry(350, 250, 500, 500)
        self.setup_ui()
        self.load_teacher_profile()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        self.title_label = QLabel("Profil de l'Enseignant")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(style.TITLE_STYLE)

        self.name_label = QLabel()
        self.gender_label = QLabel()
        self.specialization_label = QLabel()
        self.phone_label = QLabel()
        self.email_label = QLabel()
        self.address_label = QLabel()
        self.hire_date_label = QLabel()
        self.diploma_label = QLabel()
        self.experience_label = QLabel()
        self.notes_label = QLabel()

        self.back_button = QPushButton("🔙 Retour")
        self.back_button.setStyleSheet(style.BUTTON_STYLE)
        self.back_button.clicked.connect(self.close)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.gender_label)
        self.layout.addWidget(self.specialization_label)
        self.layout.addWidget(self.phone_label)
        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.address_label)
        self.layout.addWidget(self.hire_date_label)
        self.layout.addWidget(self.diploma_label)
        self.layout.addWidget(self.experience_label)
        self.layout.addWidget(self.notes_label)
        self.layout.addStretch()
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    def load_teacher_profile(self):
        try:
            teacher = teacher_model.get_teacher_by_id(self.teacher_id)
            if teacher:
                self.name_label.setText(f"👤 Nom : {teacher[2]}")
                self.gender_label.setText(f"🚻 Sexe : {teacher[3]}")
                self.specialization_label.setText(f"📚 Spécialité : {teacher[4]}")
                self.phone_label.setText(f"📞 Téléphone : {teacher[5]}")
                self.email_label.setText(f"📧 Email : {teacher[6]}")
                self.address_label.setText(f"🏠 Adresse : {teacher[7]}")
                self.hire_date_label.setText(f"📅 Date Embauche : {teacher[8]}")
                self.diploma_label.setText(f"🎓 Diplôme : {teacher[9]}")
                self.experience_label.setText(f"⌛ Années d'expérience : {teacher[10]}")
                self.notes_label.setText(f"📝 Notes : {teacher[11]}")
        except Exception as e:
            self.name_label.setText(f"Erreur : {str(e)}")
