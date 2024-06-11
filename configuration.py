import os
import yaml
import time
import socket
import random


class Configuration:
    def __init__(self, filename):
        self.C = {}
        self.filename = filename

    def configure(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(script_directory, self.filename)

        try:
            with open(self.filename, 'r') as file:
                config = yaml.load(file, Loader=yaml.FullLoader)
        except FileNotFoundError:
            a = input("file not found, do you want to create the default config file(y/n)")
            if a == 'y':
                self.create_configfile()
                with open(self.filename, 'r') as file:
                    config = yaml.load(file, Loader=yaml.FullLoader)
                print(f"default config file created: {self.filename}")
            else:
                raise FileNotFoundError

        self.validate_config(config)
        self.populate_config(config)

        return self.C

    def create_configfile(self):
        receiver_host = '0.0.0.0'
        receive_port = 5000
        name = socket.gethostname()
        discovery_timeout = 1.0

        send_port = self.find_available_port()
        discovery_port = 5000
        discovery_timeout = 1.0

        c = {
            'Receiver': {
                'RECEIVER_HOST': receiver_host,
                'RECEIVE_PORT': receive_port,
                'NAME': name,
                'PATH': None,
                'USER_INTERFACE_MODULE': 'QtGUI',
                'USER_INTERFACE_CLASS': 'QtWindow',
                'START_SERVER_MODULE': 'DefaultStartServer',
                'START_SERVER_CLASS': 'DefaultStartServerImplementation',
                'DOWNLOAD_MANAGER_MODULE': 'DownloadManager',
                'DOWNLOAD_MANAGER_CLASS': 'DownloadManagerImplementation',
            },

            'Sender': {
                'SEND_PORT': send_port,
                'DISCOVERY_PORT': discovery_port,
                'DISCOVERY_TIMEOUT': discovery_timeout,
                'NAME': name,
                'DISCOVER_RECEIVER_MODULE': 'DefaultDiscoveringImplementation',
                'DISCOVER_RECEIVER_CLASS': 'DefaultDiscoveringImplementation',
                'SENDING_FILE_MODULE': 'DefaultSendingFileImplementation',
                'SENDING_FILE_CLASS': 'DefaultSendingFileImplementation',
                'UI_MODULE': 'TkinterGUI',
                'UI_CLASS': 'GUIHandler'
            }
        }

        config = {
            'Settings': {
                'Receiver': {
                    'receiver_host': c['Receiver']['RECEIVER_HOST'],
                    'receive_port': c['Receiver']['RECEIVE_PORT'],
                    'name': c['Receiver']['NAME'],
                    'path': c['Receiver']['PATH']
                },
                'Sender': {
                    'send_port': c['Sender']['SEND_PORT'],
                    'discovery_port': c['Sender']['DISCOVERY_PORT'],
                    'discovery_timeout': c['Sender']['DISCOVERY_TIMEOUT'],
                    'name': c['Sender']['NAME']
                }
            },

            'Module': {
                'Receiver': {
                    'user_interface_module': c['Receiver']['USER_INTERFACE_MODULE'],
                    'user_interface_class': c['Receiver']['USER_INTERFACE_CLASS'],
                    'start_server_module': c['Receiver']['START_SERVER_MODULE'],
                    'start_server_class': c['Receiver']['START_SERVER_CLASS'],
                    'download_manager_module': c['Receiver']['DOWNLOAD_MANAGER_MODULE'],
                    'download_manager_class': c['Receiver']['DOWNLOAD_MANAGER_CLASS']
                },

                'Sender': {
                    'discover_receiver_module': c['Sender']['DISCOVER_RECEIVER_MODULE'],
                    'discover_receiver_class': c['Sender']['DISCOVER_RECEIVER_CLASS'],
                    'sending_file_module': c['Sender']['SENDING_FILE_MODULE'],
                    'sending_file_class': c['Sender']['SENDING_FILE_CLASS'],
                    'user_interface_module': c['Sender']['UI_MODULE'],
                    'user_interface_class': c['Sender']['UI_CLASS']
                }
            }
        }

        with open(self.filename, 'w') as configfile:
            yaml.dump(config, configfile)

    def validate_config(self, config):
        self.validate_port(config, 'Receiver', 'receive_port')
        self.validate_port(config, 'Sender', 'send_port')
        self.validate_port(config, 'Sender', 'discovery_port', 5000)
        self.validate_timeout(config, 'Sender', 'discovery_timeout')

    def populate_config(self, config):
        self.C['Receiver']['receiver_host'] = config['Settings']['Receiver']['receiver_host']
        self.C['Receiver']['name'] = config['Settings']['Receiver']['name']
        self.C['Receiver']['path'] = config['Settings']['Receiver']['path']
        self.C['Receiver']['user_interface_module'] = config['Module']['Receiver']['user_interface_module']
        self.C['Receiver']['user_interface_class'] = config['Module']['Receiver']['user_interface_class']
        self.C['Receiver']['start_server_module'] = config['Module']['Receiver']['start_server_module']
        self.C['Receiver']['start_server_class'] = config['Module']['Receiver']['start_server_class']
        self.C['Receiver']['download_manager_module'] = config['Module']['Receiver']['download_manager_module']
        self.C['Receiver']['download_manager_class'] = config['Module']['Receiver']['download_manager_class']

        self.C['Sender']['name'] = config['Settings']['Receiver']['name']
        self.C['Sender']['discover_receiver_module'] = config['Module']['Sender']['discover_receiver_module']
        self.C['Sender']['discover_receiver_class'] = config['Module']['Sender']['discover_receiver_class']
        self.C['Sender']['sending_file_module'] = config['Module']['Sender']['sending_file_module']
        self.C['Sender']['sending_file_class'] = config['Module']['Sender']['sending_file_class']
        self.C['Sender']['user_interface_module'] = config['Module']['Sender']['user_interface_module']
        self.C['Sender']['user_interface_class'] = config['Module']['Sender']['user_interface_class']

    def validate_port(self, config, section, port_name, default=None):
        try:
            port = config['Settings'][section][port_name]
            if not isinstance(port, int):
                raise ValueError(f"Invalid '{port_name}' value. It must be an integer.")
            if not (1024 <= port <= 65535):
                raise ValueError(f"Invalid '{port_name}' value. It must be between 1024 and 65535.")
            self.C.setdefault(section, {})[port_name] = port
        except KeyError:
            if default is None:
                port = self.find_available_port()
            else:
                port = 5000
            self.C.setdefault(section, {})[port_name] = port
            print(f"The value of '{port_name}' is missing. The default value of {port} will be used as the {port_name}")

    def validate_timeout(self, config, section, timeout_name):
        try:
            timeout = config['Settings'][section][timeout_name]
            if not (isinstance(timeout, int) or isinstance(timeout, float)):
                raise ValueError(f"Invalid '{timeout_name}' value. It must be an integer or a float.")
            if not (0.1 <= timeout <= 10.0):
                raise ValueError(f"Invalid '{timeout_name}' value. It must be between 0.1 and 10.0.")
            self.C.setdefault(section, {})[timeout_name] = timeout
        except KeyError:
            timeout = 1.0
            self.C.setdefault(section, {})[timeout_name] = timeout
            print(f"The value of '{timeout_name}' is missing. The default value of {timeout} will be used as the {timeout_name}")

    def find_available_port(self, timeout=10):
        start_time = time.time()
        while True:
            port = self.generate_random_port()
            if not self.is_port_in_use(port) and self.is_port_available(port):
                return port

            if time.time() - start_time > timeout:
                raise TimeoutError(f"Timeout exceeded ({timeout} seconds) while finding an available port.")

    @staticmethod
    def is_port_available(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
            except OSError:
                return False
            return True

    @staticmethod
    def generate_random_port():
        return random.randint(1024, 49151)

    @staticmethod
    def is_port_in_use(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
            except OSError:
                return True
            return False


def get_config():
    return Configuration('Config.yaml').configure()