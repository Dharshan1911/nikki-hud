import sys

from PyQt6.QtWidgets import QApplication

from widgets.chat_window import ChatWindow

app = QApplication(sys.argv)

window = ChatWindow()

window.show()

sys.exit(app.exec())
