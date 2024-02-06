from abc import ABC, abstractmethod


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
