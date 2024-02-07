import socket
import sys
import threading
import time
from PyQt6 import QtWidgets as Q
from PyQt6.QtCore import Qt
from abc import ABC, abstractmethod


# TODO: fix this wtf error
class StartServerBase(ABC):
    @abstractmethod
    def start_server(self, *args, **kwargs):
        """
        start a server to send the receiving file
        """
        raise NotImplementedError

    @abstractmethod
    def broadcast_receiver_discovery(self, *args, **kwargs):
        """
        Broadcast receiver discovery
        :param port:
        :param name: name of the receiver account
        :return:
        """
        raise NotImplementedError


# TODO: add the UI for reciever
class ReceiverWindow(Q.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"Reciever")
        self.setGeometry(500, 200, 300, 400)

        self.message_label = Q.QLabel("", self)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = Q.QVBoxLayout(self)
        layout.addWidget(self.message_label)

    def update_message(self, message):
        self.message_label.setText(message)


class DefaultStartServerImplementation(StartServerBase):
    def __init__(self):
        self.server_socket = None
        self.client_socket = None
        self.broadcast_flag = True

    def start_server(self, host, port, name, parent=NotImplemented):
        flag = True
        while flag:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.server_socket.bind((host, port))
                flag = False
            except OSError:
                # self.receiver_window.update_message(f"the port is not free yet, please wait few seconds ...")
                print(f"the port is not free yet, please wait few seconds ...")
                time.sleep(5)

        self.server_socket.listen()

        # self.receiver_window.update_message(f"server listserver_status_signal = pyqtSignal(str)ening on {host}:{port}**")
        print(f"server listening on {host}:{port}")

        discovery = threading.Thread(target=self.broadcast_receiver_discovery, args=(port, name))
        discovery.start()

        self.client_socket, client_address = self.server_socket.accept()
        # self.receiver_window.update_message(f"Connection established with {client_address}")
        print(f"Connection established with {client_address[0]}")

        recv = self.client_socket.recv(1024).decode('utf-8')
        url = recv.split('|')[0]
        name = recv.split('|')[1]
        return url, name, client_address[0]

    def send_success_message(self):
        self.client_socket.send("1".encode('utf-8'))

    def server_close(self):
        self.client_socket.close()
        self.server_socket.close()
        self.broadcast_flag = False
        sys.exit()

    def broadcast_receiver_discovery(self, port, name):
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        while self.broadcast_flag:
            message = name.encode('utf-8')
            broadcast_socket.sendto(message, ('<broadcast>', port))
            time.sleep(5)
