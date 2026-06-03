from PyQt6.QtWidgets import QApplication, QLabel
import sys

app = QApplication(sys.argv)

label = QLabel("Nikki HUD Online")
label.resize(300, 100)
label.show()

sys.exit(app.exec())
