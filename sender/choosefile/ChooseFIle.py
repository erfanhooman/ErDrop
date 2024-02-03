from abc import ABC, abstractmethod


class ChooseFileBase(ABC):
    @abstractmethod
    def pathfinder(self):
        """
        :return: the path of the file user choose
        """
        raise NotImplementedError