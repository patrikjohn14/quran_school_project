# frontend/teachers/add_teacher_window.py

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QFormLayout, QMessageBox, QComboBox, QDateEdit
)
from PyQt5.QtCore import Qt, QDate
from frontend import style
from backend import teacher_model

class AddTeacherWindow(QWidget):
    def __init__(self, teacher_id=None):
        super().__init__()
        self.teacher_id = teacher_id  # None pour ajouter, sinon ID pour modifier
        self.setWindowTitle("Ajouter / Modifier Enseignant")
        self.setGeometry(300, 300, 500, 600)
        self.setup_ui()
        
        if self.teacher_id:
            self.load_teacher_data()

    def setup_ui(self):
        title = QLabel("Ajouter un Enseignant" if not self.teacher_id else "Modifier Enseignant")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(style.TITLE_STYLE)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nom et prénom")
        self.name_input.setStyleSheet(style.INPUT_STYLE)

        self.gender_input = QComboBox()
        self.gender_input.addItems(["Homme", "Femme"])
        self.gender_input.setStyleSheet(style.INPUT_STYLE)

        self.specialization_input = QComboBox()
        self.specialization_input.addItems(["Tajweed", "Fiqh", "Arabe", "Aqida", "Tafsir", "Hadith"])
        self.specialization_input.setStyleSheet(style.INPUT_STYLE)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Téléphone")
        self.phone_input.setStyleSheet(style.INPUT_STYLE)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setStyleSheet(style.INPUT_STYLE)

        self.address_input = QTextEdit()
        self.address_input.setPlaceholderText("Adresse complète")
        self.address_input.setStyleSheet(style.INPUT_STYLE)

        self.hire_date_input = QDateEdit()
        self.hire_date_input.setCalendarPopup(True)
        self.hire_date_input.setDate(QDate.currentDate())
        self.hire_date_input.setStyleSheet(style.INPUT_STYLE)

        self.diploma_input = QLineEdit()
        self.diploma_input.setPlaceholderText("Diplôme principal")
        self.diploma_input.setStyleSheet(style.INPUT_STYLE)

        self.experience_input = QLineEdit()
        self.experience_input.setPlaceholderText("Années d'expérience")
        self.experience_input.setStyleSheet(style.INPUT_STYLE)

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Notes (facultatif)")
        self.notes_input.setStyleSheet(style.INPUT_STYLE)

        save_button = QPushButton("Enregistrer")
        save_button.setStyleSheet(style.BUTTON_STYLE)
        save_button.clicked.connect(self.save_teacher)

        form_layout = QFormLayout()
        form_layout.addRow("Nom Prénom:", self.name_input)
        form_layout.addRow("Sexe:", self.gender_input)
        form_layout.addRow("Spécialisation:", self.specialization_input)
        form_layout.addRow("Téléphone:", self.phone_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Adresse:", self.address_input)
        form_layout.addRow("Date Embauche:", self.hire_date_input)
        form_layout.addRow("Diplôme:", self.diploma_input)
        form_layout.addRow("Années d'expérience:", self.experience_input)
        form_layout.addRow("Notes:", self.notes_input)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addWidget(save_button)
        layout.addStretch()
        self.setLayout(layout)

    def load_teacher_data(self):
        teacher = teacher_model.get_teacher_by_id(self.teacher_id)
        if teacher:
            self.name_input.setText(teacher[2])
            self.gender_input.setCurrentText(teacher[3])
            self.specialization_input.setCurrentText(teacher[4])
            self.phone_input.setText(teacher[5])
            self.email_input.setText(teacher[6])
            self.address_input.setText(teacher[7])
            if teacher[8]:
                self.hire_date_input.setDate(QDate.fromString(str(teacher[8]), "yyyy-MM-dd"))
            self.diploma_input.setText(teacher[9])
            self.experience_input.setText(str(teacher[10]))
            self.notes_input.setText(teacher[11])

    def save_teacher(self):
        full_name = self.name_input.text()
        gender = self.gender_input.currentText()
        specialization = self.specialization_input.currentText()
        phone_number = self.phone_input.text()
        email = self.email_input.text()
        address = self.address_input.toPlainText()
        hire_date = self.hire_date_input.date().toString("yyyy-MM-dd")
        diploma = self.diploma_input.text()
        years_experience = self.experience_input.text()
        notes = self.notes_input.toPlainText()

        if not full_name or not phone_number:
            QMessageBox.warning(self, "Erreur", "Nom et téléphone sont obligatoires.")
            return

        data = (full_name, gender, specialization, phone_number, email, address, hire_date, diploma, years_experience, notes)

        try:
            if self.teacher_id:
                teacher_model.update_teacher(self.teacher_id, data)
                QMessageBox.information(self, "Succès", "Enseignant modifié avec succès.")
            else:
                teacher_model.add_teacher(data)
                QMessageBox.information(self, "Succès", "Enseignant ajouté avec succès.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur : {str(e)}")
