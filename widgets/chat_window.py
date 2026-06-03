from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QLineEdit,
)

from core.ollama_client import ask_nikki


class ChatWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Nikki Chat")
        self.resize(600, 400)

        layout = QVBoxLayout()

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        self.input = QLineEdit()

        self.send_btn = QPushButton("Send")

        self.send_btn.clicked.connect(
            self.send_message
        )

        layout.addWidget(self.chat)
        layout.addWidget(self.input)
        layout.addWidget(self.send_btn)

        self.setLayout(layout)

    def send_message(self):

        prompt = self.input.text()

        if not prompt:
            return

        self.chat.append(f"You: {prompt}")

        reply = ask_nikki(prompt)

        self.chat.append(f"Nikki: {reply}\n")

        self.input.clear()
