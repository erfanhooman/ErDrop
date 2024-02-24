import sys
import time

from sender.sender import UIHandler
from receiver.receiver import Receiver
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QDialog, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Er-Drop")

        # Create buttons
        self.button1 = QPushButton("Send File")
        self.button2 = QPushButton("Receive File")

        # Add buttons to layout
        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connect button clicks to functions
        self.button1.clicked.connect(self.handle_send)
        self.button2.clicked.connect(self.handle_receive)

    def handle_send(self):
        sender = UIHandler(self)
        self.close()

    def handle_receive(self):
        # self.window = Window("Receive File", "Waiting for Sender")
        # self.window.show()
        Receiver(self)


class Window(QDialog):
    def __init__(self, title, text):
        super().__init__()

        self.setWindowTitle(title)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.initial_message = text
        self.update_message(self.initial_message)

    def update_message(self, message):
        self.label.setText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
