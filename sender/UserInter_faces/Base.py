from abc import ABC, abstractmethod


class UIHandlerBase(ABC):
    """
    handler of the UI
    Contain three part :
        __init__ :
        1. choose the file function , the function that ask for the file path and return the name and filepath
        2. show the receiver list, and update it constantly, and you can choose the receiver
        3. send the file to the user after choosing the receiver by the user
    """
    @abstractmethod
    def __init__(self, Sender):
        """
        To do call the three essential method and other method
        :param Sender: the class of Sender for finding and connecting and sending file to receivers
        """
        self.Sender = Sender

    @abstractmethod
    def choose_file(self):
        """
        choose the file method , the function that ask for the file path
        :return: tuple of : name, filepath
        """

    @abstractmethod
    def select_and_send(self, event):
        """
        select the user and send the file to it
        """

    @abstractmethod
    def window_refresh(self):
        """
        constantly refresh the page and show the newest receivers
        """