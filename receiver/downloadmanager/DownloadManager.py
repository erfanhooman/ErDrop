import os
import socket

import requests
from tqdm import tqdm

from receiver.downloadmanager.DownloadManagerBase import DownloadManager

class DownloadManagerImplementation(DownloadManager):
    def __init__(self, url, name, client_ip, path=None, chunk_size=8192):
        self.client_ip = client_ip
        self.url = url
        self.name = name
        if path is None:
            path = self.default_path()
        self.chunk_size = chunk_size
        self.fullpath = self.get_fullpath(path)

    def get_fullpath(self, path):
        fullpath = os.path.join(path, self.name)
        if os.path.exists(fullpath):
            filename, file_extension = os.path.splitext(fullpath)
            count = 1
            while os.path.exists(f"{filename}({count}){file_extension}"):
                count += 1
            fullpath = f"{filename}({count}){file_extension}"
        return fullpath

    def download_file(self):
        try:
            response_ip = socket.gethostbyname(socket.gethostname())
            response = requests.get(url=self.url, stream=True, verify=False)
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))

            with open(self.fullpath, 'wb') as file, tqdm(
                    desc=f"Downloading {self.fullpath.split('/')[-1]}", total=total_size,
                    unit='B', unit_scale=True
            ) as pbar:
                for chunk in response.iter_content(chunk_size=self.chunk_size):
                    if chunk:
                        file.write(chunk)
                        pbar.update(len(chunk))

            print(f"Downloaded: {self.fullpath.split('/')[-1]} to {self.fullpath}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file: {e}")
            return False

    @staticmethod
    def default_path():
        return os.getcwd()
