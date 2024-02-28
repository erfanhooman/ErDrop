from abc import ABC, abstractmethod

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget, QPushButton


class QtWindow(QWidget):
    connection_accepted = pyqtSignal()
    connection_rejected = pyqtSignal()

    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(250, 100)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.accept_button = QPushButton("Accept")
        self.reject_button = QPushButton("Rejec # Continue listening for next connection attemptt")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.accept_button)
        layout.addWidget(self.reject_button)
        self.setLayout(layout)

        self.initial_message = "Please Wait few Second..."
        self.update_message(self.initial_message)

        self.accept_button.clicked.connect(self.accept_connection)
        self.reject_button.clicked.connect(self.reject_connection)

        self.hide_buttons()

    def update_message(self, message):
        self.label.setText(message)

    def show_buttons(self):
        self.accept_button.show()
        self.reject_button.show()

    def hide_buttons(self):
        self.accept_button.hide()
        self.reject_button.hide()

    def accept_connection(self):
        self.connection_accepted.emit()

    def reject_connection(self):
        self.connection_rejected.emit()

