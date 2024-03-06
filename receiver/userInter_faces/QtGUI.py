from abc import ABC, abstractmethod

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget, QPushButton


class QtWindow(QWidget):
    def __init__(self, title):
        super().__init__()
        self.accept = False
        self.reject = False

        self.setWindowTitle(title)
        self.setFixedSize(450, 100)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.accept_button = QPushButton("Accept")
        self.reject_button = QPushButton("Reject")

        self.accept_button.clicked.connect(self.accept_clicked)
        self.reject_button.clicked.connect(self.reject_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.accept_button)
        layout.addWidget(self.reject_button)
        self.setLayout(layout)

        self.initial_message = "Please Wait few Second..."
        self.update_message(self.initial_message)

        self.hide_buttons()

    def update_message(self, message):
        self.label.setText(message)

    def show_buttons(self):
        self.accept_button.show()
        self.reject_button.show()

    def hide_buttons(self):
        self.accept_button.hide()
        self.reject_button.hide()

    def accept_clicked(self):
        self.accept = True

    def reject_clicked(self):
        self.reject = True
