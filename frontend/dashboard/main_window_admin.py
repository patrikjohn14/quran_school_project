# frontend/dashboard/main_window_admin.py

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout
from PyQt5.QtCore import Qt
from frontend import style

class MainWindowAdmin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard Administrateur")
        self.setGeometry(200, 200, 750, 550)
        self.setup_ui()

    def setup_ui(self):
        title_label = QLabel("Bienvenue Administrateur 👑")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(style.TITLE_STYLE)

        students_button = QPushButton("📚 Gestion des Élèves")
        teachers_button = QPushButton("👨‍🏫 Gestion des Enseignants")
        courses_button = QPushButton("📖 Gestion des Cours")
        attendance_button = QPushButton("✅ Gestion des Présences")
        grades_button = QPushButton("📝 Gestion des Notes")
        stats_button = QPushButton("📊 Statistiques Générales")
        export_button = QPushButton("📤 Exportations PDF")
        logout_button = QPushButton("🔓 Déconnexion")

        buttons = [students_button, teachers_button, courses_button, attendance_button, grades_button, stats_button, export_button, logout_button]
        for button in buttons:
            button.setFixedSize(180, 80)
            button.setStyleSheet(style.BUTTON_STYLE)

        students_button.clicked.connect(self.open_students)
        teachers_button.clicked.connect(self.open_teachers)
        courses_button.clicked.connect(self.open_courses)
        attendance_button.clicked.connect(self.open_attendance)
        grades_button.clicked.connect(self.open_grades)
        stats_button.clicked.connect(self.open_statistics)
        export_button.clicked.connect(self.open_export)
        logout_button.clicked.connect(self.logout)

        grid_layout = QGridLayout()
        grid_layout.addWidget(students_button, 0, 0)
        grid_layout.addWidget(teachers_button, 0, 1)
        grid_layout.addWidget(courses_button, 0, 2)
        grid_layout.addWidget(attendance_button, 1, 0)
        grid_layout.addWidget(grades_button, 1, 1)
        grid_layout.addWidget(stats_button, 1, 2)
        grid_layout.addWidget(export_button, 2, 0)
        grid_layout.addWidget(logout_button, 2, 1)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addLayout(grid_layout)
        layout.addStretch()

        self.setLayout(layout)

    def open_students(self):
        from frontend.students.students_window import StudentsWindow
        self.students_window = StudentsWindow()
        self.students_window.show()
        self.close()

    def open_teachers(self):
        from frontend.teachers.teachers_window import TeachersWindow
        self.teachers_window = TeachersWindow()
        self.teachers_window.show()
        self.close()

    def open_courses(self):
        from frontend.courses.courses_window import CoursesWindow
        self.courses_window = CoursesWindow()
        self.courses_window.show()
        self.close()

    def open_attendance(self):
        from frontend.attendance.attendance_window import AttendanceWindow
        self.attendance_window = AttendanceWindow()
        self.attendance_window.show()
        self.close()

    def open_grades(self):
        from frontend.admin.admin_grades_window import AdminGradesWindow
        self.grades_window = AdminGradesWindow()
        self.grades_window.show()
        self.close()

    def open_statistics(self):
        from frontend.admin.admin_statistics_window import AdminStatisticsWindow
        self.stats_window = AdminStatisticsWindow()
        self.stats_window.show()
        self.close()

    def open_export(self):
        from frontend.admin.admin_export_window import AdminExportWindow
        self.export_window = AdminExportWindow()
        self.export_window.show()
        self.close()

    def logout(self):
        from frontend.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
