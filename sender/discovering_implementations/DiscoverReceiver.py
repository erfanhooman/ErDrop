from abc import ABC, abstractmethod


class DiscoveringImplementationBase(ABC):
    @abstractmethod
    def modify_discovery_socket(self, receive_port: int, timeout: int):
        """
        start a server to discover the receiver
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def update_receivers(self, receivers: dict):
        """
        update the list of the receivers
        :param receivers: the dict of receivers
        :receivers : {
            'receiver name: {
                'ip': receiver_ip,
                'last_updated_time': last updated time
        }'
        """
        raise NotImplementedError
