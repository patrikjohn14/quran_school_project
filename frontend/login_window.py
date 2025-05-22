# frontend/login_window.py

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from frontend import style
from backend import user_model

# Variable globale pour stocker l'ID utilisateur connecté
global_user_id = None

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion - École Coranique")
        self.setGeometry(400, 200, 400, 300)
        self.setup_ui()

    def setup_ui(self):
        title = QLabel("Se connecter à l'application")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(style.TITLE_STYLE)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        self.username_input.setStyleSheet(style.INPUT_STYLE)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(style.INPUT_STYLE)

        login_button = QPushButton("Se connecter")
        login_button.setStyleSheet(style.BUTTON_STYLE)
        login_button.clicked.connect(self.login)

        register_button = QPushButton("Créer un compte")
        register_button.setStyleSheet(style.BUTTON_STYLE)
        register_button.clicked.connect(self.register)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.addWidget(register_button)
        self.setLayout(layout)

    def login(self):
        global global_user_id

        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")
            return

        user = user_model.verify_user(username, password)
        if user:
            user_id, role = user
            global_user_id = user_id  # 🔥 Stocker l'user_id globalement

            if role == "admin":
                from frontend.dashboard.main_window_admin import MainWindowAdmin
                self.window = MainWindowAdmin()
            elif role == "teacher":
                from frontend.dashboard.main_window_teacher import MainWindowTeacher
                self.window = MainWindowTeacher()
            else:
                QMessageBox.warning(self, "Erreur", "Rôle inconnu.")
                return

            self.window.show()
            self.close()
        else:
            QMessageBox.critical(self, "Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

    def register(self):
        from frontend.register_window import RegisterWindow
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()
