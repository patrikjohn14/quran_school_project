# frontend/teachers/teachers_window.py

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit
)
from PyQt5.QtCore import Qt
from frontend import style
from backend import teacher_model

class TeachersWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Enseignants")
        self.setGeometry(200, 200, 1000, 650)

        self.teachers_per_page = 10
        self.current_page = 0
        self.all_teachers = []

        self.setup_ui()
        self.load_teachers()

    def setup_ui(self):
        title_label = QLabel("Liste des Enseignants")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(style.TITLE_STYLE)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Rechercher un enseignant...")
        self.search_input.textChanged.connect(self.update_display)
        self.search_input.setStyleSheet(style.INPUT_STYLE)

        add_button = QPushButton("➕ Ajouter un enseignant")
        add_button.setStyleSheet(style.BUTTON_STYLE)
        add_button.clicked.connect(self.add_teacher)

        back_button = QPushButton("🏠 Retour à l'accueil")
        back_button.setStyleSheet(style.BUTTON_STYLE)
        back_button.clicked.connect(self.return_to_dashboard)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Sexe", "Spécialité", "Téléphone", "Actions"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.prev_button = QPushButton("⬅️ Précédent")
        self.next_button = QPushButton("Suivant ➡️")
        self.prev_button.setStyleSheet(style.BUTTON_STYLE)
        self.next_button.setStyleSheet(style.BUTTON_STYLE)
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)

        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(back_button)

        pagination_layout = QHBoxLayout()
        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addWidget(self.next_button)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(self.search_input)
        layout.addLayout(button_layout)
        layout.addWidget(self.table)
        layout.addLayout(pagination_layout)
        self.setLayout(layout)

    def load_teachers(self):
        try:
            self.all_teachers = teacher_model.get_all_teachers()
            self.update_display()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur de chargement : {str(e)}")

    def update_display(self):
        search_text = self.search_input.text().lower()
        filtered_teachers = [
            t for t in self.all_teachers if search_text in t[2].lower() or search_text in t[5]
        ]

        start = self.current_page * self.teachers_per_page
        end = start + self.teachers_per_page
        teachers_to_show = filtered_teachers[start:end]

        self.table.setRowCount(0)

        for row_num, teacher in enumerate(teachers_to_show):
            self.table.insertRow(row_num)
            self.table.setItem(row_num, 0, QTableWidgetItem(str(teacher[0])))
            self.table.setItem(row_num, 1, QTableWidgetItem(teacher[2]))
            self.table.setItem(row_num, 2, QTableWidgetItem(teacher[3]))
            self.table.setItem(row_num, 3, QTableWidgetItem(teacher[4]))
            self.table.setItem(row_num, 4, QTableWidgetItem(teacher[5]))

            # Actions
            action_layout = QHBoxLayout()
            profile_button = QPushButton("📋")
            edit_button = QPushButton("✏️")
            delete_button = QPushButton("🗑️")

            for btn in [profile_button, edit_button, delete_button]:
                btn.setFixedSize(30, 30)
                btn.setStyleSheet(style.BUTTON_STYLE)

            profile_button.clicked.connect(lambda _, id=teacher[0]: self.view_profile(id))
            edit_button.clicked.connect(lambda _, id=teacher[0]: self.edit_teacher(id))
            delete_button.clicked.connect(lambda _, id=teacher[0]: self.delete_teacher(id))

            container = QWidget()
            container_layout = QHBoxLayout(container)
            container_layout.addWidget(profile_button)
            container_layout.addWidget(edit_button)
            container_layout.addWidget(delete_button)
            container_layout.setContentsMargins(0, 0, 0, 0)
            self.table.setCellWidget(row_num, 5, container)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_display()

    def next_page(self):
        max_pages = len(self.all_teachers) // self.teachers_per_page
        if len(self.all_teachers) % self.teachers_per_page == 0:
            max_pages -= 1
        if self.current_page < max_pages:
            self.current_page += 1
            self.update_display()

    def add_teacher(self):
        from frontend.teachers.add_teacher_window import AddTeacherWindow
        self.add_window = AddTeacherWindow()
        self.add_window.show()
        self.add_window.closeEvent = self.reload_on_close

    def edit_teacher(self, teacher_id):
        from frontend.teachers.add_teacher_window import AddTeacherWindow
        self.edit_window = AddTeacherWindow(teacher_id)
        self.edit_window.show()
        self.edit_window.closeEvent = self.reload_on_close

    def delete_teacher(self, teacher_id):
        confirmation = QMessageBox.question(self, "Confirmer", "Supprimer cet enseignant ?", QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            try:
                teacher_model.delete_teacher(teacher_id)
                QMessageBox.information(self, "Succès", "Enseignant supprimé.")
                self.load_teachers()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur : {str(e)}")

    def view_profile(self, teacher_id):
        from frontend.teachers.teacher_profile_window import TeacherProfileWindow
        self.profile_window = TeacherProfileWindow(teacher_id)
        self.profile_window.show()

    def reload_on_close(self, event):
        self.load_teachers()
        event.accept()

    def return_to_dashboard(self):
        from frontend.main_window import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()
