import socket
import time

from sender.discovering_implementations.DiscoverReceiverBase import DiscoveringImplementationBase


class DefaultDiscoveringImplementation(DiscoveringImplementationBase):
    def __init__(self, receive_port, timeout):
        self.discovery_socket = None
        self.receivers = {}
        self.modify_discovery_socket(receive_port, timeout)

    def modify_discovery_socket(self, receive_port, timeout):
        self.discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.discovery_socket.settimeout(timeout)
        self.discovery_socket.bind(('', receive_port))

    def update_receivers(self, receivers):
        self.receivers = receivers
        if self.receivers:
            for disconnected_receiver in self.disconnected_receivers(3):
                del self.receivers[disconnected_receiver]

        try:
            data, addr = self.discovery_socket.recvfrom(1024)
        except socket.timeout:
            data, addr = None, None
        if data is not None:
            receiver_ip = addr[0]
            receiver_name = data.decode('utf-8')
            self.receivers[receiver_name] = {'ip': receiver_ip, "last_updated_time": time.time()}
            return receiver_name, receiver_ip
        else:
            return None, None

    def disconnected_receivers(self, sec=60):
        current_time = time.time()
        to_remove = []

        for receiver_name, info in self.receivers.items():
            if current_time - info['last_updated_time'] > sec:
                to_remove.append(receiver_name)
        return to_remove

    def close_discovery_socket(self):
        self.discovery_socket.close()