import os
import socket

import requests
from tqdm import tqdm


class DownloadManagerImplementation:
    def __init__(self, url, name, client_ip, path=None, chunk_size=8192):
        self.client_ip = client_ip
        self.url = url
        self.name = name
        if path is None:
            path = self.default_path()
        self.path = path
        self.chunk_size = chunk_size
        self.fullpath = self.get_fullpath(self.path)
        self.headers = self.get_headers()

    def get_fullpath(self, path):
        return os.path.join(path, self.name)

    def get_headers(self):
        if os.path.exists(self.fullpath):
            return {'Range': f'bytes={os.path.getsize(self.path)}'}
        return {}

    def download_file(self):
        try:
            # TODO: auth the reciever
            response_ip = socket.gethostbyname(socket.gethostname())
            if True:
                response = requests.get(url=self.url, headers=self.headers, stream=True, verify=True)
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
            else:
                print("Download file stopped, the client didnt authorized")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Error downloading file: {e}")
            return False

    @staticmethod
    def default_path():
        return os.getcwd()
