import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

from sender.sender import UIHandler
from receiver.receiver import Receiver


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ErDrop")
        self.setGeometry(100, 100, 400, 200)

        self.sender_button = QPushButton("Sender", self)
        self.receiver_button = QPushButton("Receiver", self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.sender_button)
        layout.addWidget(self.receiver_button)

        self.sender_button.clicked.connect(self.create_sender_instance)
        self.receiver_button.clicked.connect(self.create_receiver_instance)

    def create_sender_instance(self):
        sender = UIHandler(self)
        self.close()

    def create_receiver_instance(self):
        self.close()
        r = Receiver()
        r.start_server()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())