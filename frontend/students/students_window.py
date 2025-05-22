# frontend/students/students_window.py

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit
)
from PyQt5.QtCore import Qt
from frontend import style
from backend.db_connection import get_connection

class StudentsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Élèves")
        self.setGeometry(200, 200, 1000, 650)

        self.students_per_page = 10
        self.current_page = 0
        self.all_students = []

        self.setup_ui()
        self.load_students()

    def setup_ui(self):
        # Titre
        title_label = QLabel("Liste des élèves")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(style.TITLE_STYLE)

        # Barre de recherche
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Rechercher un élève par nom ou téléphone...")
        self.search_input.textChanged.connect(self.update_display)
        self.search_input.setStyleSheet(style.INPUT_STYLE)

        # Bouton ajouter
        add_button = QPushButton("➕ Ajouter un élève")
        add_button.setStyleSheet(style.BUTTON_STYLE)
        add_button.clicked.connect(self.add_student)

        # Bouton retour accueil
        back_button = QPushButton("🏠 Retour à l'accueil")
        back_button.setStyleSheet(style.BUTTON_STYLE)
        back_button.clicked.connect(self.return_to_dashboard)

        # Tableau
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nom Prénom", "Date de Naissance", "Téléphone", "Adresse", "Actions"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Boutons pagination
        self.prev_button = QPushButton("⬅️ Précédent")
        self.next_button = QPushButton("Suivant ➡️")
        self.prev_button.setStyleSheet(style.BUTTON_STYLE)
        self.next_button.setStyleSheet(style.BUTTON_STYLE)
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)

        # Layout
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

    def load_students(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, full_name, birth_date, phone_number, address, student_class FROM students")
            self.all_students = cursor.fetchall()
            cursor.close()
            conn.close()

            self.update_display()

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur de chargement : {str(e)}")

    def update_display(self):
        search_text = self.search_input.text().lower()
        filtered_students = [s for s in self.all_students if search_text in s[1].lower() or search_text in s[3]]

        start = self.current_page * self.students_per_page
        end = start + self.students_per_page
        students_to_show = filtered_students[start:end]

        self.table.setRowCount(0)

        for row_num, row_data in enumerate(students_to_show):
            self.table.insertRow(row_num)
            for col_num, data in enumerate(row_data[:-1]):  # sans la classe ici
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(data)))

            # Actions (Profil, Modifier, Supprimer)
            action_layout = QHBoxLayout()
            profile_button = QPushButton("📋")
            edit_button = QPushButton("✏️")
            delete_button = QPushButton("🗑️")

            for btn in [profile_button, edit_button, delete_button]:
                btn.setFixedSize(30, 30)
                btn.setStyleSheet(style.BUTTON_STYLE)

            profile_button.clicked.connect(lambda _, id=row_data[0]: self.view_profile(id))
            edit_button.clicked.connect(lambda _, id=row_data[0]: self.edit_student(id))
            delete_button.clicked.connect(lambda _, id=row_data[0]: self.delete_student(id))

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
        max_pages = len(self.all_students) // self.students_per_page
        if len(self.all_students) % self.students_per_page == 0:
            max_pages -= 1
        if self.current_page < max_pages:
            self.current_page += 1
            self.update_display()

    def add_student(self):
        from frontend.students.add_student_window import AddStudentWindow
        self.add_window = AddStudentWindow()
        self.add_window.show()
        self.add_window.closeEvent = self.reload_on_close

    def edit_student(self, student_id):
        from frontend.students.add_student_window import AddStudentWindow
        self.edit_window = AddStudentWindow(student_id)
        self.edit_window.show()
        self.edit_window.closeEvent = self.reload_on_close

    def delete_student(self, student_id):
        confirmation = QMessageBox.question(self, "Confirmer", "Êtes-vous sûr de vouloir supprimer cet élève ?", QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
                conn.commit()
                cursor.close()
                conn.close()
                QMessageBox.information(self, "Succès", "Élève supprimé.")
                self.load_students()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur de suppression : {str(e)}")

    def view_profile(self, student_id):
        from frontend.students.student_profile_window import StudentProfileWindow
        self.profile_window = StudentProfileWindow(student_id)
        self.profile_window.show()

    def reload_on_close(self, event):
        self.load_students()
        event.accept()

    def return_to_dashboard(self):
        from frontend.main_window import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()
