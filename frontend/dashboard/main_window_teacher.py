# frontend/dashboard/main_window_teacher.py

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout
from PyQt5.QtCore import Qt
from frontend import style

class MainWindowTeacher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard Enseignant")
        self.setGeometry(200, 200, 500, 400)
        self.setup_ui()

    def setup_ui(self):
        title_label = QLabel("Bienvenue Enseignant 👨‍🏫")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(style.TITLE_STYLE)

        courses_button = QPushButton("📖 Mes Cours")
        attendance_button = QPushButton("✅ Mes Présences")
        grades_button = QPushButton("📝 Mes Notes")
        logout_button = QPushButton("🔓 Déconnexion")

        buttons = [courses_button, attendance_button, grades_button, logout_button]
        for button in buttons:
            button.setFixedSize(160, 80)
            button.setStyleSheet(style.BUTTON_STYLE)

        courses_button.clicked.connect(self.open_courses)
        attendance_button.clicked.connect(self.open_attendance)
        grades_button.clicked.connect(self.open_grades)
        logout_button.clicked.connect(self.logout)

        grid_layout = QGridLayout()
        grid_layout.addWidget(courses_button, 0, 0)
        grid_layout.addWidget(attendance_button, 0, 1)
        grid_layout.addWidget(grades_button, 1, 0)
        grid_layout.addWidget(logout_button, 1, 1)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addLayout(grid_layout)
        layout.addStretch()

        self.setLayout(layout)

    def open_courses(self):
        pass

    def open_attendance(self):
        # (À préparer juste après pour MyPrésences)
        pass

    def open_grades(self):
        # (À préparer juste après pour MyNotes)
        pass

    def logout(self):
       pass