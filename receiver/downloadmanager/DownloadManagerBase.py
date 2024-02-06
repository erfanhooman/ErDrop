from abc import ABC, abstractmethod


class DownloadManager(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        """
        Download a file from the given url and save it into the path

        :param chunk_size: the size of each chunk,
            download file in few chunk
        """
        raise NotImplementedError

    @abstractmethod
    def get_headers(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def download_file(self, *args, **kwargs):
        raise NotImplementedError
