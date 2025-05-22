# frontend/register_window.py

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QMessageBox
from PyQt5.QtCore import Qt
from frontend import style
from backend import user_model

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Créer un compte")
        self.setGeometry(400, 200, 400, 350)
        self.setup_ui()

    def setup_ui(self):
        title = QLabel("Créer un nouveau compte")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(style.TITLE_STYLE)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        self.username_input.setStyleSheet(style.INPUT_STYLE)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(style.INPUT_STYLE)

        self.role_input = QComboBox()
        self.role_input.addItems(["admin", "teacher"])
        self.role_input.setStyleSheet(style.INPUT_STYLE)

        register_button = QPushButton("S'inscrire")
        register_button.setStyleSheet(style.BUTTON_STYLE)
        register_button.clicked.connect(self.register)

        back_button = QPushButton("Retour à la connexion")
        back_button.setStyleSheet(style.BUTTON_STYLE)
        back_button.clicked.connect(self.back_to_login)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel("Choisir un rôle :"))
        layout.addWidget(self.role_input)
        layout.addWidget(register_button)
        layout.addWidget(back_button)
        self.setLayout(layout)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_input.currentText()

        if not username or not password:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")
            return

        try:
            user_model.register_user(username, password, role)
            QMessageBox.information(self, "Succès", "Compte créé avec succès. Connectez-vous maintenant.")
            self.back_to_login()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la création du compte : {str(e)}")

    def back_to_login(self):
        from frontend.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
