# frontend/admin/admin_export_window.py

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from frontend import style
from backend import export_model

class AdminExportWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exportations PDF - Admin")
        self.setGeometry(250, 150, 600, 400)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout()

        title = QLabel("📤 Exportations de Rapports PDF")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(style.TITLE_STYLE)

        export_attendance_button = QPushButton("✅ Exporter Présences (PDF)")
        export_attendance_button.setStyleSheet(style.BUTTON_STYLE)
        export_attendance_button.clicked.connect(self.export_attendance)

        export_grades_button = QPushButton("📝 Exporter Notes (PDF)")
        export_grades_button.setStyleSheet(style.BUTTON_STYLE)
        export_grades_button.clicked.connect(self.export_grades)

        back_button = QPushButton("🏠 Retour au Dashboard")
        back_button.setStyleSheet(style.BUTTON_STYLE)
        back_button.clicked.connect(self.back_to_dashboard)

        self.layout.addWidget(title)
        self.layout.addWidget(export_attendance_button)
        self.layout.addWidget(export_grades_button)
        self.layout.addWidget(back_button)

        self.setLayout(self.layout)

    def export_attendance(self):
        result = export_model.export_attendance_to_pdf()
        if result:
            QMessageBox.information(self, "Succès", "Présences exportées en PDF avec succès.")
        else:
            QMessageBox.warning(self, "Erreur", "Erreur lors de l'export des présences.")

    def export_grades(self):
        result = export_model.export_grades_to_pdf()
        if result:
            QMessageBox.information(self, "Succès", "Notes exportées en PDF avec succès.")
        else:
            QMessageBox.warning(self, "Erreur", "Erreur lors de l'export des notes.")

    def back_to_dashboard(self):
        from frontend.dashboard.main_window_admin import MainWindowAdmin
        self.dashboard = MainWindowAdmin()
        self.dashboard.show()
        self.close()
