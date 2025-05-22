# frontend/admin/admin_statistics_window.py

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from frontend import style
from backend import attendance_model, grades_model

class AdminStatisticsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Statistiques - Admin")
        self.setGeometry(250, 150, 600, 400)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        title = QLabel("📊 Statistiques Générales")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(style.TITLE_STYLE)

        self.total_students_label = QLabel()
        self.total_courses_label = QLabel()
        self.total_attendance_label = QLabel()
        self.average_grade_label = QLabel()

        for label in [self.total_students_label, self.total_courses_label, self.total_attendance_label, self.average_grade_label]:
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(style.LABEL_STYLE)

        refresh_button = QPushButton("🔄 Rafraîchir Statistiques")
        refresh_button.setStyleSheet(style.BUTTON_STYLE)
        refresh_button.clicked.connect(self.load_statistics)

        back_button = QPushButton("🏠 Retour au Dashboard")
        back_button.setStyleSheet(style.BUTTON_STYLE)
        back_button.clicked.connect(self.back_to_dashboard)

        self.layout.addWidget(title)
        self.layout.addWidget(self.total_students_label)
        self.layout.addWidget(self.total_courses_label)
        self.layout.addWidget(self.total_attendance_label)
        self.layout.addWidget(self.average_grade_label)
        self.layout.addWidget(refresh_button)
        self.layout.addWidget(back_button)

        self.setLayout(self.layout)

        self.load_statistics()

    def load_statistics(self):
        total_students = attendance_model.get_total_students()
        total_courses = attendance_model.get_total_courses()
        total_attendance = attendance_model.get_total_attendance_records()
        average_grade = grades_model.get_average_grade()

        self.total_students_label.setText(f"Nombre total d'élèves : {total_students}")
        self.total_courses_label.setText(f"Nombre total de cours : {total_courses}")
        self.total_attendance_label.setText(f"Nombre total de présences enregistrées : {total_attendance}")
        self.average_grade_label.setText(f"Note moyenne générale : {average_grade:.2f} / 20")

    def back_to_dashboard(self):
        from frontend.dashboard.main_window_admin import MainWindowAdmin
        self.dashboard = MainWindowAdmin()
        self.dashboard.show()
        self.close()
