# frontend/admin/admin_grades_window.py

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout
from PyQt5.QtCore import Qt
from frontend import style
from backend import grades_model, student_model, course_model

class AdminGradesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Notes - Admin")
        self.setGeometry(250, 150, 800, 550)
        self.setup_ui()

    def setup_ui(self):
        title = QLabel("Ajouter une Note 📚")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(style.TITLE_STYLE)

        # Formulaire pour ajouter une note
        self.student_input = QComboBox()
        self.course_input = QComboBox()
        self.grade_input = QLineEdit()
        self.grade_input.setPlaceholderText("Note sur 20")

        self.load_students()
        self.load_courses()

        add_button = QPushButton("Ajouter la Note")
        add_button.setStyleSheet(style.BUTTON_STYLE)
        add_button.clicked.connect(self.add_grade)

        form_layout = QFormLayout()
        form_layout.addRow("Élève :", self.student_input)
        form_layout.addRow("Cours :", self.course_input)
        form_layout.addRow("Note :", self.grade_input)
        form_layout.addWidget(add_button)

        # Tableau pour voir toutes les notes
        self.grades_table = QTableWidget()
        self.grades_table.setColumnCount(4)
        self.grades_table.setHorizontalHeaderLabels(["ID", "Élève", "Cours", "Note sur 20"])
        self.grades_table.horizontalHeader().setStretchLastSection(True)
        self.grades_table.cellChanged.connect(self.update_grade)

        # Boutons
        refresh_button = QPushButton("🔄 Rafraîchir")
        refresh_button.setStyleSheet(style.BUTTON_STYLE)
        refresh_button.clicked.connect(self.load_grades)

        delete_button = QPushButton("🗑️ Supprimer la note sélectionnée")
        delete_button.setStyleSheet(style.BUTTON_STYLE)
        delete_button.clicked.connect(self.delete_grade)

        back_button = QPushButton("🏠 Retour au Dashboard")
        back_button.setStyleSheet(style.BUTTON_STYLE)
        back_button.clicked.connect(self.back_to_dashboard)

        button_layout = QHBoxLayout()
        button_layout.addWidget(refresh_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(back_button)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addWidget(QLabel("Liste des Notes existantes 📜"))
        layout.addWidget(self.grades_table)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.load_grades()

    def load_students(self):
        students = student_model.get_all_students()
        self.student_map = {}
        self.student_input.clear()
        for student in students:
            self.student_input.addItem(student[1])  # Nom complet
            self.student_map[student[1]] = student[0]  # ID

    def load_courses(self):
        courses = course_model.get_all_courses()
        self.course_map = {}
        self.course_input.clear()
        for course in courses:
            self.course_input.addItem(course[1])  # Nom du cours
            self.course_map[course[1]] = course[0]  # ID

    def add_grade(self):
        student_name = self.student_input.currentText()
        course_name = self.course_input.currentText()
        grade_value = self.grade_input.text()

        if not grade_value:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer une note.")
            return

        try:
            grade = float(grade_value)
            if grade < 0 or grade > 20:
                QMessageBox.warning(self, "Erreur", "La note doit être entre 0 et 20.")
                return

            student_id = self.student_map.get(student_name)
            course_id = self.course_map.get(course_name)
            grades_model.add_grade(student_id, course_id, grade)

            QMessageBox.information(self, "Succès", "Note ajoutée avec succès.")
            self.grade_input.clear()
            self.load_grades()
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un nombre valide.")

    def load_grades(self):
        self.grades_table.blockSignals(True)  # pour éviter appel inutile à update_grade
        self.grades_table.setRowCount(0)
        grades = grades_model.get_all_grades_with_ids()
        for row_num, grade in enumerate(grades):
            self.grades_table.insertRow(row_num)
            self.grades_table.setItem(row_num, 0, QTableWidgetItem(str(grade[0])))  # ID de la note
            self.grades_table.setItem(row_num, 1, QTableWidgetItem(grade[1]))  # Nom élève
            self.grades_table.setItem(row_num, 2, QTableWidgetItem(grade[2]))  # Cours
            note_item = QTableWidgetItem(str(grade[3]))
            note_item.setFlags(note_item.flags() | Qt.ItemIsEditable)  # Rendre la note éditable
            self.grades_table.setItem(row_num, 3, note_item)
        self.grades_table.blockSignals(False)

    def update_grade(self, row, column):
        if column != 3:  # Seule la colonne des notes est éditable
            return

        grade_id_item = self.grades_table.item(row, 0)
        new_grade_item = self.grades_table.item(row, column)

        try:
            grade_id = int(grade_id_item.text())
            new_grade = float(new_grade_item.text())

            if new_grade < 0 or new_grade > 20:
                QMessageBox.warning(self, "Erreur", "La note doit être entre 0 et 20.")
                self.load_grades()
                return

            grades_model.update_grade(grade_id, new_grade)
            QMessageBox.information(self, "Succès", "Note mise à jour avec succès.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la mise à jour : {e}")
            self.load_grades()

    def delete_grade(self):
        selected_row = self.grades_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une note à supprimer.")
            return

        grade_id_item = self.grades_table.item(selected_row, 0)
        if grade_id_item:
            grade_id = int(grade_id_item.text())
            grades_model.delete_grade(grade_id)
            QMessageBox.information(self, "Succès", "Note supprimée avec succès.")
            self.load_grades()

    def back_to_dashboard(self):
        from frontend.dashboard.main_window_admin import MainWindowAdmin
        self.dashboard = MainWindowAdmin()
        self.dashboard.show()
        self.close()
