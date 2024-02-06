from abc import ABC, abstractmethod


class ServerImplementationBase(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        """
        - Server Implementation to run server and put the file on it
        :param file_path: the location of file
        :param send_port: the port to put the file on it
        :param filename: the name of file
        """
        raise NotImplementedError

    @abstractmethod
    def server_implement(self, *args, **kwargs):
        """
        - Start a server to share a file
        :param directory: the location of file
        :param port: the port to put the file on it
        """
        raise NotImplementedError

    @abstractmethod
    def stop_server(self, *args, **kwargs):
        """
        - close the server at the end of the program
        """
        raise NotImplementedError

    @abstractmethod
    def connect_and_send(self, *args, **kwargs):
        """
        connect and send file to receiver
        :param receiver: dict of receiver items
        :param receiver_port: port of the receiver
        :param server: server that we use to connect the sender and receiver
        """
        raise NotImplementedError
