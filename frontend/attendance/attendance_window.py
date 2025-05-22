# frontend/attendance/attendance_window.py

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QDateEdit, QComboBox, QListWidget, QListWidgetItem, QMessageBox, QCheckBox
)
from PyQt5.QtCore import Qt, QDate
from frontend import style
from backend import course_model, attendance_model
from backend.db_connection import get_connection

class AttendanceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion de la Présence")
        self.setGeometry(250, 200, 600, 600)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        self.title_label = QLabel("Marquer la présence par cours")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(style.TITLE_STYLE)

        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setStyleSheet(style.INPUT_STYLE)

        self.course_input = QComboBox()
        self.course_input.setStyleSheet(style.INPUT_STYLE)
        self.load_courses()

        self.load_students_button = QPushButton("📋 Charger les élèves")
        self.load_students_button.setStyleSheet(style.BUTTON_STYLE)
        self.load_students_button.clicked.connect(self.load_students)

        self.view_present_button = QPushButton("👁️ Voir les Présents")
        self.view_present_button.setStyleSheet(style.BUTTON_STYLE)
        self.view_present_button.clicked.connect(self.view_present_students)

        self.students_list = QListWidget()
        self.students_list.setStyleSheet(style.INPUT_STYLE)

        self.save_button = QPushButton("💾 Enregistrer la présence")
        self.save_button.setStyleSheet(style.BUTTON_STYLE)
        self.save_button.clicked.connect(self.save_attendance)

        self.back_button = QPushButton("🏠 Retour au Dashboard")
        self.back_button.setStyleSheet(style.BUTTON_STYLE)
        self.back_button.clicked.connect(self.back_to_dashboard)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(QLabel("Sélectionner la date:"))
        self.layout.addWidget(self.date_input)
        self.layout.addWidget(QLabel("Sélectionner le cours:"))
        self.layout.addWidget(self.course_input)
        self.layout.addWidget(self.load_students_button)
        self.layout.addWidget(self.view_present_button)
        self.layout.addWidget(self.students_list)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.back_button)  # Bouton retour ajouté ici

        self.setLayout(self.layout)

    def load_courses(self):
        self.courses = course_model.get_all_courses()
        self.course_map = {}
        for course in self.courses:
            course_label = f"{course[1]} ({course[3]})"
            self.course_input.addItem(course_label)
            self.course_map[course_label] = course[0]

    def load_students(self):
        self.students_list.clear()
        course_label = self.course_input.currentText()
        if not course_label:
            return
        course_id = self.course_map.get(course_label)
        course = course_model.get_course_by_id(course_id)
        class_name = course[3]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, full_name
            FROM students
            WHERE student_class = %s
        """, (class_name,))
        students = cursor.fetchall()
        cursor.close()
        conn.close()

        self.students_checkboxes = {}
        for student in students:
            item = QListWidgetItem()
            widget = QWidget()
            layout = QHBoxLayout(widget)
            checkbox = QCheckBox(student[1])
            layout.addWidget(checkbox)
            layout.setAlignment(Qt.AlignLeft)
            layout.setContentsMargins(0, 0, 0, 0)
            self.students_list.addItem(item)
            self.students_list.setItemWidget(item, widget)
            self.students_checkboxes[student[0]] = checkbox

    def save_attendance(self):
        date = self.date_input.date().toString("yyyy-MM-dd")
        course_label = self.course_input.currentText()
        if not course_label:
            return
        course_id = self.course_map.get(course_label)

        for student_id, checkbox in self.students_checkboxes.items():
            status = 'present' if checkbox.isChecked() else 'absent'
            attendance_model.add_attendance(student_id, course_id, date, status)

        QMessageBox.information(self, "Succès", "Présence enregistrée avec succès.")
        self.close()

    def view_present_students(self):
        course_label = self.course_input.currentText()
        if not course_label:
            return
        course_id = self.course_map.get(course_label)
        date = self.date_input.date().toString("yyyy-MM-dd")

        from frontend.attendance.view_present_students_window import ViewPresentStudentsWindow
        self.view_present_window = ViewPresentStudentsWindow(course_id, date)
        self.view_present_window.show()

    def back_to_dashboard(self):
        from frontend.dashboard.main_window_admin import MainWindowAdmin
        self.dashboard = MainWindowAdmin()
        self.dashboard.show()
        self.close()
