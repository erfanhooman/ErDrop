import socket
import sys
import threading
import time
from PyQt6.QtCore import QObject
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


class DefaultStartServerImplementation:
    def __init__(self, ui):
        self.client_address = None
        self.connection_accepted = False
        self.connection_info = None
        self.ui = ui
        self.server_socket = None
        self.client_socket = None
        self.broadcast_flag = True

    def start_server(self, host, port, name):
        flag = True
        while flag:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.server_socket.bind((host, port))
                flag = False
            except OSError:
                self.ui.update_message("Getting Your System Ready...")
                time.sleep(5)

        self.server_socket.listen()

        print(f"server listening on {host}:{port}")
        self.ui.update_message("Waiting for Reciever...")

        discovery = threading.Thread(target=self.broadcast_receiver_discovery, args=(port, name))
        discovery.start()

        while True:
            self.client_socket, self.client_address = self.server_socket.accept()
            self.ui.update_message(f"Do you want to accept connection from {self.client_address}?")
            self.ui.show_buttons()

            self.ui.connection_accepted.connect(self.on_connection_accepted)
            self.ui.connection_accepted.connect(self.on_connection_rejected)
            print("1")
            if self.connection_info:
                self.ui.hide_buttons()
                return self.connection_info

    def on_connection_accepted(self):
        print("Connection accepted")
        recv = self.client_socket.recv(1024).decode('utf-8')
        url = recv.split('|')[0]
        name = recv.split('|')[1]
        client_ip = self.client_address[0]
        self.connection_info = (url, name, client_ip)

    def on_connection_rejected(self):
        print("Connection rejected.")
        self.client_socket.close()
        self.ui.hide_buttons()

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