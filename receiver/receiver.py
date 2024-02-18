from configuration import get_config

# --- Temp --- #
from PyQt6 import QtWidgets as Q


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
        url, name, client_ip = self.start_server()
        result = self.download_manager(url, name, client_ip, PATH)
        if result:
            print("Download Successfully")
            self.server.send_success_message()
            self.server.server_close()
        else:
            print("Download Failed TryAgain")

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
