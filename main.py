from PyQt5.QtWidgets import QApplication
import sys
from frontend.login_window import LoginWindow

def main():
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
