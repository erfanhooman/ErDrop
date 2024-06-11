from abc import ABC, abstractmethod


class DownloadManager(ABC):
    @abstractmethod
    def __init__(self, url, name, client_ip, path=None, *args, **kwargs):
        """
        Download a file from the given url and save it into the path

        :param chunk_size: the size of each chunk,
            download file in few chunk
        """
        raise NotImplementedError

    @abstractmethod
    def download_file(self, *args, **kwargs):
        """
        Download a file from the path in self.url, store it in the path in a self.path
        in the name of the self.name
        the function must return True if the download succeed and False if download failed
        """
        raise NotImplementedError