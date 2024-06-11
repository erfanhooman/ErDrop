import socket
from configuration import get_config

config = get_config()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except Exception as e:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

HOST = get_local_ip()

SEND_PORT = config['Sender']['send_port']
DISCOVERY_PORT = config['Sender']['discovery_port']
DISCOVERY_TIMEOUT = config['Sender']['discovery_timeout']
NAME = config['Sender']['name']

DISCOVER_RECEIVER_MODULE = config['Sender']['discover_receiver_module']
DISCOVER_RECEIVER_CLASS = config['Sender']['discover_receiver_class']
SENDING_FILE_MODULE = config['Sender']['sending_file_module']
SENDING_FILE_CLASS = config['Sender']['sending_file_class']

UI_MODULE = config['Sender']['user_interface_module']
UI_CLASS = config['Sender']['user_interface_class']


def dynamic_import(section_name, module_name, class_name):
    try:
        print(section_name, module_name, class_name)
        module = __import__(f"sender.{section_name}.{module_name}")
        DynamicClass = getattr(getattr(getattr(module, section_name), module_name), class_name)
        return DynamicClass
    except TypeError as e:
        raise ValueError(f"Something Wrong with config file {section_name} part")


class Sender:
    def __init__(self, file_path: str, file_name: str, ui):
        self.receivers = {}
        self.discovering = None
        self.setup_discovery_socket(DISCOVERY_PORT)

        self.file_name = file_name
        self.sending_server = None
        self.setup_sending_file(file_path, SEND_PORT, self.file_name, ui, NAME)

    def setup_discovery_socket(self, receive_port):
        """
        setup server to find the potential receivers
        """
        DynamicClass = dynamic_import('discovering_implementations',
                                      DISCOVER_RECEIVER_MODULE, DISCOVER_RECEIVER_CLASS)
        self.discovering = DynamicClass(receive_port, DISCOVERY_TIMEOUT)

    def update_receivers_list(self):
        """
        Update the Dictionary of the receivers each time this function called
        """
        return self.discovering.update_receivers(self.receivers)

    def end_discovering(self):
        """
        end the looking for new receivers and close the server
        :return:
        """
        self.discovering.close_discovery_socket()

    def setup_sending_file(self, filepath, port, file_name, ui, name):
        """
        setup to send the file to receivers
        :param filepath: the path of the file we want to send
        :param port: the port we want to send during it
        :param file_name: name of the file we want to send to it
        """
        DynamicClass = dynamic_import('sending_file_implementations',
                                      SENDING_FILE_MODULE, SENDING_FILE_CLASS)
        self.sending_server = DynamicClass(filepath, port, file_name, ui, name)

    def connect_to_receiver(self, receiver_ip, receiver_port):
        """
        connect to specific receiver to send the file to it
        :param receiver_ip: the ip of the receives
        :param receiver_port: the port we send file on it
        """
        self.sending_server.connect_and_send(receiver_ip, receiver_port, HOST)


def UIHandler(parent):
    """
    UI Handler
    """
    DynamicClass = dynamic_import('userInter_faces',
                                  UI_MODULE, UI_CLASS)
    DynamicClass(Sender, DISCOVERY_PORT, parent)