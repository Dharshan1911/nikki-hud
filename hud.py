import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor

from core.system_monitor import get_stats
from widgets.chat_window import ChatWindow

class NikkiHUD(QWidget):

    def __init__(self):
        super().__init__()

        self.resize(260, 280)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.radius = 40
        self.growing = True

        self.status_label = QLabel("NIKKI ONLINE", self)
        self.status_label.move(75, 150)

        self.cpu_label = QLabel("CPU: 0%", self)
        self.cpu_label.move(80, 180)

        self.ram_label = QLabel("RAM: 0 GB", self)
        self.ram_label.move(80, 205)

        self.listen_label = QLabel("Listening...", self)
        self.listen_label.move(80, 230)

        self.orb_timer = QTimer()
        self.orb_timer.timeout.connect(self.animate)
        self.orb_timer.start(50)

        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(1000)

        self.update_stats()
        self.chat_window = ChatWindow()

    def update_stats(self):

        stats = get_stats()

        self.cpu_label.setText(
            f"CPU: {stats['cpu']}%"
        )

        self.ram_label.setText(
            f"RAM: {stats['ram']} GB"
        )

    def animate(self):

        if self.growing:
            self.radius += 1
            if self.radius > 50:
                self.growing = False
        else:
            self.radius -= 1
            if self.radius < 40:
                self.growing = True

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center_x = self.width() // 2
        center_y = 80

        glow = QColor(0, 180, 255, 80)

        painter.setBrush(glow)
        painter.setPen(Qt.PenStyle.NoPen)

        painter.drawEllipse(
            center_x - self.radius,
            center_y - self.radius,
            self.radius * 2,
            self.radius * 2,
        )

        core = QColor(0, 220, 255)

        painter.setBrush(core)

        painter.drawEllipse(
            center_x - 25,
            center_y - 25,
            50,
            50,
        )

    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = event.globalPosition().toPoint() - self.oldPos

        self.move(
            self.x() + delta.x(),
            self.y() + delta.y()
        )

        self.oldPos = event.globalPosition().toPoint()

    def mouseDoubleClickEvent(self, event):

        if self.chat_window.isVisible():
            self.chat_window.hide()
        else:
            self.chat_window.show()
            self.chat_window.raise_()
            self.chat_window.activateWindow()

app = QApplication(sys.argv)

hud = NikkiHUD()

screen = app.primaryScreen().availableGeometry()

hud.move(
    screen.width() - 320,
    screen.height() - 380
)

hud.show()

sys.exit(app.exec())
