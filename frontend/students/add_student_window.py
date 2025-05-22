# frontend/students/add_student_window.py

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QFormLayout, QMessageBox, QDateEdit, QComboBox
)
from PyQt5.QtCore import Qt, QDate
from frontend import style
from backend.db_connection import get_connection

class AddStudentWindow(QWidget):
    def __init__(self, student_id=None):
        super().__init__()
        self.student_id = student_id  # None pour ajouter, sinon ID pour modifier
        self.setWindowTitle("Ajouter / Modifier Élève")
        self.setGeometry(300, 300, 400, 500)
        self.setup_ui()
        
        if self.student_id:
            self.load_student_data()

    def setup_ui(self):
        # Titre
        title = QLabel("Ajouter un Élève" if not self.student_id else "Modifier Élève")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(style.TITLE_STYLE)

        # Formulaire
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nom et prénom")
        self.name_input.setStyleSheet(style.INPUT_STYLE)

        self.birth_date_input = QDateEdit()
        self.birth_date_input.setCalendarPopup(True)
        self.birth_date_input.setDate(QDate.currentDate())
        self.birth_date_input.setStyleSheet(style.INPUT_STYLE)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Téléphone")
        self.phone_input.setStyleSheet(style.INPUT_STYLE)

        self.address_input = QTextEdit()
        self.address_input.setPlaceholderText("Adresse complète")
        self.address_input.setStyleSheet(style.INPUT_STYLE)

        self.class_input = QComboBox()
        self.class_input.addItems(["Classe 1", "Classe 2", "Classe 3", "Classe 4", "Classe 5"])
        self.class_input.setStyleSheet(style.INPUT_STYLE)

        # Bouton sauvegarde
        save_button = QPushButton("Enregistrer")
        save_button.setStyleSheet(style.BUTTON_STYLE)
        save_button.clicked.connect(self.save_student)

        # Layout formulaire
        form_layout = QFormLayout()
        form_layout.addRow("Nom Prénom:", self.name_input)
        form_layout.addRow("Date de naissance:", self.birth_date_input)
        form_layout.addRow("Téléphone:", self.phone_input)
        form_layout.addRow("Adresse:", self.address_input)
        form_layout.addRow("Classe:", self.class_input)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addWidget(save_button)
        layout.addStretch()

        self.setLayout(layout)

    def load_student_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT full_name, birth_date, phone_number, address, student_class FROM students WHERE id = %s", (self.student_id,))
            student = cursor.fetchone()
            cursor.close()
            conn.close()

            if student:
                self.name_input.setText(student[0])
                self.birth_date_input.setDate(QDate.fromString(str(student[1]), "yyyy-MM-dd"))
                self.phone_input.setText(student[2])
                self.address_input.setText(student[3])
                if student[4] in [self.class_input.itemText(i) for i in range(self.class_input.count())]:
                    index = self.class_input.findText(student[4])
                    self.class_input.setCurrentIndex(index)

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur de chargement : {str(e)}")

    def save_student(self):
        full_name = self.name_input.text()
        birth_date = self.birth_date_input.date().toString("yyyy-MM-dd")
        phone_number = self.phone_input.text()
        address = self.address_input.toPlainText()
        student_class = self.class_input.currentText()

        if not full_name or not phone_number or not address or not student_class:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            if self.student_id:  # Modifier
                cursor.execute("""
                    UPDATE students 
                    SET full_name = %s, birth_date = %s, phone_number = %s, address = %s, student_class = %s
                    WHERE id = %s
                """, (full_name, birth_date, phone_number, address, student_class, self.student_id))
            else:  # Ajouter
                cursor.execute("""
                    INSERT INTO students (full_name, birth_date, phone_number, address, student_class)
                    VALUES (%s, %s, %s, %s, %s)
                """, (full_name, birth_date, phone_number, address, student_class))

            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Succès", "Élève enregistré avec succès.")
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'enregistrement : {str(e)}")
