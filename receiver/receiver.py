import threading
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel
from configuration import get_config
from PyQt6 import QtWidgets as Q
from PyQt6.QtCore import Qt


config = get_config()

RECEIVER_HOST = config['Receiver']['receiver_host']
RECEIVER_PORT = config['Receiver']['receive_port']
Name = config['Receiver']['name']
PATH = config['Receiver']['path']

START_SERVER_MODULE = config['Receiver']['start_server_module']
START_SERVER_CLASS = config['Receiver']['start_server_class']

DOWNLOAD_MANAGER_MODULE = config['Receiver']['download_manager_module']
DOWNLOAD_MANAGER_CLASS = config['Receiver']['download_manager_class']


def dynamic_import(section_name, module_name, class_name):
    try:
        module = __import__(f'receiver.{section_name}.{module_name}')
        DynamicClass = getattr(getattr(getattr(module, section_name), module_name), class_name)
        return DynamicClass
    except TypeError as e:
        raise ValueError(f"Something Wrong with config file {section_name} part")


class Receiver:
    def __init__(self, parent):
        self.parent = parent
        self.ui_handler()

    def ui_handler(self):
        self.parent.window = Window("Receive File", "Waiting for Sender")
        self.parent.window.show()

        def start():
            url, name, client_ip = self.start_server()
            result = self.download_manager(url, name, client_ip, PATH)
            if result:
                self.parent.window.update_message("Download Successfully")
                self.server.send_success_message()
                self.server.server_close()
            else:
                self.parent.window.update_message("Download Failed TryAgain")
                print("Download Failed TryAgain")

        threading.Thread(target=start, args=()).start()

    def start_server(self):
        """
        Broadcast a server of receiver to discover by the sender
        """
        DynamicClass = dynamic_import('startserver',
                                      START_SERVER_MODULE, START_SERVER_CLASS)
        self.server = DynamicClass()
        url, name, client_ip = self.server.start_server(RECEIVER_HOST, RECEIVER_PORT, Name)
        return url, name, client_ip

    @staticmethod
    def download_manager(url, name, client_ip, path=None, chunk_size=8192):
        """
        Download a file from the given url and save it into the path

        :param chunk_size: the size of each chunk,
            download file in few chunk
        """
        DynamicClass = dynamic_import('downloadmanager',
                                      DOWNLOAD_MANAGER_MODULE, DOWNLOAD_MANAGER_CLASS)
        result = DynamicClass(url, name, client_ip, path, chunk_size).download_file()
        return result


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


class ReceiverWindow(Q.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reciever Waiting...")
        self.setGeometry(500, 200, 300, 400)
        self.list_widget = Q.QListWidget(self)
        # self.message_label = Q.QLabel("Waiting for server to start...", self)
        layout = Q.QVBoxLayout(self)
        layout.addWidget(self.list_widget)

    def update_message(self, message):
        self.message_label.setText(message)
