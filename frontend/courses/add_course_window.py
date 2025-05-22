# frontend/courses/add_course_window.py

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QFormLayout, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt
from frontend import style
from backend import course_model, teacher_model

class AddCourseWindow(QWidget):
    def __init__(self, course_id=None):
        super().__init__()
        self.course_id = course_id
        self.setWindowTitle("Ajouter / Modifier Cours")
        self.setGeometry(300, 300, 500, 500)
        self.setup_ui()
        if self.course_id:
            self.load_course_data()

    def setup_ui(self):
        title = QLabel("Ajouter un Cours" if not self.course_id else "Modifier Cours")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(style.TITLE_STYLE)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nom du cours")
        self.name_input.setStyleSheet(style.INPUT_STYLE)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Description du cours")
        self.description_input.setStyleSheet(style.INPUT_STYLE)

        self.class_input = QLineEdit()
        self.class_input.setPlaceholderText("Nom de la classe")
        self.class_input.setStyleSheet(style.INPUT_STYLE)

        self.teacher_input = QComboBox()
        self.teacher_input.setStyleSheet(style.INPUT_STYLE)
        self.load_teachers()

        save_button = QPushButton("Enregistrer")
        save_button.setStyleSheet(style.BUTTON_STYLE)
        save_button.clicked.connect(self.save_course)

        form_layout = QFormLayout()
        form_layout.addRow("Nom du Cours:", self.name_input)
        form_layout.addRow("Description:", self.description_input)
        form_layout.addRow("Classe:", self.class_input)
        form_layout.addRow("Enseignant Responsable:", self.teacher_input)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addWidget(save_button)
        layout.addStretch()

        self.setLayout(layout)

    def load_teachers(self):
        teachers = teacher_model.get_all_teachers()
        self.teachers_map = {}
        for t in teachers:
            name = t[2]
            self.teachers_map[name] = t[0]  # { "Nom": id }
            self.teacher_input.addItem(name)

    def load_course_data(self):
        course = course_model.get_course_by_id(self.course_id)
        if course:
            self.name_input.setText(course[1])
            self.description_input.setText(course[2])
            self.class_input.setText(course[3])
            # Sélectionner enseignant
            teacher_id = course[4]
            if teacher_id:
                for i in range(self.teacher_input.count()):
                    if self.teachers_map.get(self.teacher_input.itemText(i)) == teacher_id:
                        self.teacher_input.setCurrentIndex(i)
                        break

    def save_course(self):
        name = self.name_input.text()
        description = self.description_input.toPlainText()
        class_name = self.class_input.text()
        teacher_name = self.teacher_input.currentText()
        teacher_id = self.teachers_map.get(teacher_name)

        if not name or not class_name:
            QMessageBox.warning(self, "Erreur", "Nom du cours et Classe sont obligatoires.")
            return

        data = (name, description, class_name, teacher_id)

        try:
            if self.course_id:
                course_model.update_course(self.course_id, data)
                QMessageBox.information(self, "Succès", "Cours modifié avec succès.")
            else:
                course_model.add_course(data)
                QMessageBox.information(self, "Succès", "Cours ajouté avec succès.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur : {str(e)}")
