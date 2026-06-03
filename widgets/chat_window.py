from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QLineEdit,
)
from PyQt6.QtCore import QThread, pyqtSignal

from core.ollama_client import stream_nikki


class NikkiWorker(QThread):

    chunk_received = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):

        try:

            for chunk in stream_nikki(self.prompt):
                self.chunk_received.emit(chunk)

        except Exception as e:

            self.chunk_received.emit(
                f"\n\n[ERROR] {e}"
            )

        self.finished.emit()


class ChatWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Nikki Chat")
        self.resize(600, 400)

        layout = QVBoxLayout()

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        self.input = QLineEdit()
        self.input.returnPressed.connect(
            self.send_message
        )

        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(
            self.send_message
        )

        layout.addWidget(self.chat)
        layout.addWidget(self.input)
        layout.addWidget(self.send_btn)

        self.setLayout(layout)

        self.worker = None

    def send_message(self):

        prompt = self.input.text().strip()

        if not prompt:
            return

        self.chat.append(f"\nYou: {prompt}")
        self.chat.append("\nNikki: ")

        self.input.clear()

        self.send_btn.setEnabled(False)

        self.worker = NikkiWorker(prompt)

        self.worker.chunk_received.connect(
            self.append_chunk
        )

        self.worker.finished.connect(
            self.finish_reply
        )

        self.worker.start()

    def append_chunk(self, chunk):

        cursor = self.chat.textCursor()

        cursor.movePosition(
            cursor.MoveOperation.End
        )

        cursor.insertText(chunk)

        self.chat.setTextCursor(cursor)

        self.chat.ensureCursorVisible()

    def finish_reply(self):

        self.chat.append("\n")

        self.send_btn.setEnabled(True)
