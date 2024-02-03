from abc import ABC, abstractmethod


class DownloadManager(ABC):
    @abstractmethod
    def __init__(self):
        """
        Download a file from the given url and save it into the path

        :param chunk_size: the size of each chunk,
            download file in few chunk
        """
        raise NotImplemented

    @abstractmethod
    def get_headers(self):
        raise NotImplemented

    @abstractmethod
    def download_file(self):
        raise NotImplemented
