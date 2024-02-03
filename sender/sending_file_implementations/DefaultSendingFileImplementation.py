import os
import sys
import socket
import secrets
import threading
from tqdm import tqdm

from twisted.internet import reactor, ssl
from twisted.web import resource, server

from sender.sending_file_implementations.SendingFIle import ServerImplementationBase

# TODO: increase the security of url with loging the reciever ip and check the reciever ip
# TODO: ssh key the file when you are sending the file - end to end (set ssl) *


class FileServer(resource.Resource):
    isLeaf = True

    def __init__(self, file_path):
        self.file_path = file_path

    def render_GET(self, request):
        file_path = os.path.join(self.file_path)

        if os.path.isfile(file_path):
            file = open(file_path, 'rb')
            request.setHeader(b"content-type", b"application/octet-stream")

            def send_chunk(data):
                request.write(data)
                pbar.update(len(data))

            def finish_request(_):
                pbar.close()
                request.finish()

            def error_occurred(failure):
                request.processingFailed(failure)
                request.finish()

            def read_and_send():
                data = file.read(4096)
                if data:
                    send_chunk(data)
                    reactor.callLater(0, read_and_send)
                else:
                    file.close()
                    finish_request(None)

            total_size = os.path.getsize(file_path)
            pbar = tqdm(total=total_size, desc=f"Uploading {file_path.split('/')[-1]}")

            reactor.callLater(0, read_and_send)
            return server.NOT_DONE_YET
        else:
            request.setResponseCode(404)
            request.finish()
            raise Exception("File not found")


class DefaultSendingFileImplementation(ServerImplementationBase):
    def __init__(self, file_path, send_port, filename):
        self.file_name = filename
        self.temp_dir = None
        self.send_port = send_port

        server_thread = threading.Thread(target=self.server_implement,
                                         args=(file_path, send_port))
        server_thread.start()
        self.server = None

    def server_implement(self, filepath: str, port: int):
        site = server.Site(FileServer(file_path=filepath))
        reactor.listenTCP(port, site, interface='0.0.0.0')
        reactor.run(installSignalHandlers=False)

    def _server_implement(self, filepath: str, port: int):

        ssl_dir = os.path.join(os.path.dirname(__file__), 'ssl')
        cert_path = os.path.join(ssl_dir, 'certificate.crt')
        key_path = os.path.join(ssl_dir, 'privatekey.key')

        site = server.Site(FileServer(file_path=filepath))
        cert_options = ssl.CertificateOptions.fromPEMFiles(cert_path, key_path)

        reactor.listenSSL(port, site, cert_options, interface='0.0.0.0')
        reactor.run(installSignalHandlers=False)

    def stop_server(self):
        reactor.stop()
        sys.exit()

    def connect_and_send(self, receiver, receiver_port, server):
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sender_socket.connect((receiver['ip'], receiver_port))

            authentication_token = secrets.token_urlsafe(16)
            url = f"http://{server}:{self.send_port}|{self.file_name}"
            sender_socket.send(url.encode('utf-8'))
            status = sender_socket.recv(1024).decode('utf-8')
            if status == "1":
                print("file sent Successfully")
                sender_socket.close()
                self.stop_server()

        except ValueError as ce:
            print(f"Connection Error connecting to the server: {ce}")
            sender_socket.close()
            self.stop_server()
            sys.exit()