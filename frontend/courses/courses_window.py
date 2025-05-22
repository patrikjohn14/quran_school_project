# frontend/courses/courses_window.py

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit
)
from PyQt5.QtCore import Qt
from frontend import style
from backend import course_model

class CoursesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Cours")
        self.setGeometry(200, 200, 1000, 650)

        self.courses_per_page = 10
        self.current_page = 0
        self.all_courses = []

        self.setup_ui()
        self.load_courses()

    def setup_ui(self):
        title_label = QLabel("Liste des Cours")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(style.TITLE_STYLE)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Rechercher un cours...")
        self.search_input.textChanged.connect(self.update_display)
        self.search_input.setStyleSheet(style.INPUT_STYLE)

        add_button = QPushButton("➕ Ajouter un cours")
        add_button.setStyleSheet(style.BUTTON_STYLE)
        add_button.clicked.connect(self.add_course)

        back_button = QPushButton("🏠 Retour à l'accueil")
        back_button.setStyleSheet(style.BUTTON_STYLE)
        back_button.clicked.connect(self.return_to_dashboard)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Description", "Classe", "Enseignant", "Actions"])
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

    def load_courses(self):
        try:
            self.all_courses = course_model.get_all_courses()
            self.update_display()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur de chargement : {str(e)}")

    def update_display(self):
        search_text = self.search_input.text().lower()
        filtered_courses = [
            c for c in self.all_courses if search_text in c[1].lower() or (c[3] and search_text in c[3].lower())
        ]

        start = self.current_page * self.courses_per_page
        end = start + self.courses_per_page
        courses_to_show = filtered_courses[start:end]

        self.table.setRowCount(0)

        for row_num, course in enumerate(courses_to_show):
            self.table.insertRow(row_num)
            self.table.setItem(row_num, 0, QTableWidgetItem(str(course[0])))
            self.table.setItem(row_num, 1, QTableWidgetItem(course[1]))
            self.table.setItem(row_num, 2, QTableWidgetItem(course[2] if course[2] else ""))
            self.table.setItem(row_num, 3, QTableWidgetItem(course[3] if course[3] else ""))
            self.table.setItem(row_num, 4, QTableWidgetItem(course[4] if course[4] else ""))

            action_layout = QHBoxLayout()
            students_button = QPushButton("📋")
            edit_button = QPushButton("✏️")
            delete_button = QPushButton("🗑️")

            for btn in [students_button, edit_button, delete_button]:
                btn.setFixedSize(30, 30)
                btn.setStyleSheet(style.BUTTON_STYLE)

            students_button.clicked.connect(lambda _, id=course[0]: self.view_students(id))
            edit_button.clicked.connect(lambda _, id=course[0]: self.edit_course(id))
            delete_button.clicked.connect(lambda _, id=course[0]: self.delete_course(id))

            container = QWidget()
            container_layout = QHBoxLayout(container)
            container_layout.addWidget(students_button)
            container_layout.addWidget(edit_button)
            container_layout.addWidget(delete_button)
            container_layout.setContentsMargins(0, 0, 0, 0)
            self.table.setCellWidget(row_num, 5, container)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_display()

    def next_page(self):
        max_pages = len(self.all_courses) // self.courses_per_page
        if len(self.all_courses) % self.courses_per_page == 0:
            max_pages -= 1
        if self.current_page < max_pages:
            self.current_page += 1
            self.update_display()

    def add_course(self):
        from frontend.courses.add_course_window import AddCourseWindow
        self.add_window = AddCourseWindow()
        self.add_window.show()
        self.add_window.closeEvent = self.reload_on_close

    def edit_course(self, course_id):
        from frontend.courses.add_course_window import AddCourseWindow
        self.edit_window = AddCourseWindow(course_id)
        self.edit_window.show()
        self.edit_window.closeEvent = self.reload_on_close

    def delete_course(self, course_id):
        confirmation = QMessageBox.question(self, "Confirmer", "Supprimer ce cours ?", QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            try:
                course_model.delete_course(course_id)
                QMessageBox.information(self, "Succès", "Cours supprimé.")
                self.load_courses()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur : {str(e)}")

    def view_students(self, course_id):
        from frontend.courses.course_students_window import CourseStudentsWindow
        self.students_window = CourseStudentsWindow(course_id)
        self.students_window.show()

    def reload_on_close(self, event):
        self.load_courses()
        event.accept()

    def return_to_dashboard(self):
        from frontend.main_window import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()
