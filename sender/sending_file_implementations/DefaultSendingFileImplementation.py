import os
import sys
import socket
import secrets
import threading

from OpenSSL import crypto

from twisted.internet import reactor, ssl
from twisted.web import resource, server

from sender.sending_file_implementations.SendingFIle import ServerImplementationBase


class FileServer(resource.Resource):
    isLeaf = True

    def __init__(self, file_path, progress_bar):
        self.file_path = file_path
        self.progress_bar = progress_bar

    def render_GET(self, request):
        file_path = os.path.join(self.file_path)

        if os.path.isfile(file_path):
            file = open(file_path, 'rb')
            request.setHeader(b"content-type", b"application/octet-stream")

            def send_chunk(data):
                request.write(data)
                self.progress_bar.setValue(self.progress_bar.value() + len(data))
                reactor.callLater(0, read_and_send)

            def finish_request(_):
                request.finish()

            def error_occurred(failure):
                request.processingFailed(failure)
                request.finish()

            def read_and_send():
                data = file.read(4096)
                if data:
                    send_chunk(data)
                    # reactor.callLater(0, read_and_send)
                else:
                    file.close()
                    finish_request(None)

            total_size = os.path.getsize(file_path)

            self.progress_bar.setMaximum(total_size)
            self.progress_bar.setValue(0)

            read_and_send()
            return server.NOT_DONE_YET
        else:
            request.setResponseCode(404)
            request.finish()
            raise Exception("File not found")


class DefaultSendingFileImplementation(ServerImplementationBase):
    def __init__(self, file_path, send_port, filename, ui):
        self.progress_bar = ui
        self.file_name = filename
        self.temp_dir = None
        self.send_port = send_port

        server_thread = threading.Thread(target=self.server_implement,
                                         args=(file_path, send_port))
        server_thread.start()
        self.server = None

    def _server_implement(self, filepath, port):
        site = server.Site(FileServer(file_path=filepath, progress_bar=self.progress_bar))
        reactor.listenTCP(port, site, interface='0.0.0.0')
        reactor.run()

    def server_implement(self, filepath: str, port: int):

        ssl_dir = os.path.join(os.path.dirname(__file__), 'ssl')

        private_key = crypto.PKey()
        private_key.generate_key(crypto.TYPE_RSA, 2048)

        cert = crypto.X509()
        cert.get_subject().CN = "example.com"
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(private_key)
        cert.sign(private_key, "sha256")

        site = server.Site(FileServer(file_path=filepath, progress_bar=self.progress_bar))
        cert_options = ssl.CertificateOptions(privateKey=private_key, certificate=cert)

        reactor.listenSSL(port, site, cert_options, interface='0.0.0.0')
        reactor.run(installSignalHandlers=False)

    def stop_server(self):
        reactor.stop()
        sys.exit()

    def connect_and_send(self, receiver, receiver_port, host):
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sender_socket.connect((receiver['ip'], receiver_port))
            authentication_token = secrets.token_urlsafe(16)
            url = f"https://{host}:{self.send_port}|{self.file_name}"
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
