# frontend/main_window.py

from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtCore import Qt
from frontend import style
from backend import course_model

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Page d'Accueil - École Coranique")
        self.setGeometry(200, 200, 650, 450)
        self.setup_ui()

    def setup_ui(self):
        title_label = QLabel("Bienvenue sur la plateforme de gestion scolaire")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(style.TITLE_STYLE)

        students_button = QPushButton("📚 Élèves")
        teachers_button = QPushButton("👨‍🏫 Enseignants")
        courses_button = QPushButton("📖 Cours")
        attendance_button = QPushButton("✅ Présences")
        grades_button = QPushButton("📝 Notes")
        logout_button = QPushButton("🔓 Déconnexion")

        buttons = [students_button, teachers_button, courses_button, attendance_button, grades_button, logout_button]
        for button in buttons:
            button.setFixedSize(160, 80)
            button.setStyleSheet(style.BUTTON_STYLE)

        students_button.clicked.connect(self.open_students)
        teachers_button.clicked.connect(self.open_teachers)
        courses_button.clicked.connect(self.open_courses)
        attendance_button.clicked.connect(self.open_attendance)
        grades_button.clicked.connect(self.open_grades)
        logout_button.clicked.connect(self.logout)

        self.course_input = QComboBox()
        self.course_input.setStyleSheet(style.INPUT_STYLE)
        self.load_courses()

        grid_layout = QGridLayout()
        grid_layout.addWidget(students_button, 0, 0)
        grid_layout.addWidget(teachers_button, 0, 1)
        grid_layout.addWidget(courses_button, 0, 2)
        grid_layout.addWidget(attendance_button, 1, 0)
        grid_layout.addWidget(grades_button, 1, 1)
        grid_layout.addWidget(logout_button, 1, 2)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title_label)
        main_layout.addWidget(self.course_input)
        main_layout.addLayout(grid_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

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
        # Récupérer l'ID du cours sélectionné
        course_label = self.course_input.currentText()
        if not course_label:
            return  # Si aucun cours n'est sélectionné, rien ne se passe

        course_id = self.get_course_id_from_label(course_label)
        
        from frontend.grades.grades_window import GradesWindow
        self.grades_window = GradesWindow(course_id)  # Passer course_id au constructeur
        self.grades_window.show()
        self.close()

    def get_course_id_from_label(self, label):
        # Cette fonction permet de récupérer l'ID du cours à partir de son nom
        for course in self.courses:
            if f"{course[1]} ({course[3]})" == label:  # Comparaison avec le label affiché
                return course[0]
        return None

    def logout(self):
        from frontend.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def load_courses(self):
        self.courses = course_model.get_all_courses()
        self.course_map = {}
        for course in self.courses:
            course_label = f"{course[1]} ({course[3]})"  # Nom du cours + classe
            self.course_input.addItem(course_label)
            self.course_map[course_label] = course[0]
