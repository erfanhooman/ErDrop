import sys
import threading

from sender.userInter_faces.GUIBase import UIHandlerBase
from PyQt6 import QtWidgets as Q
from PyQt6.QtCore import QTimer


class QtUIHandler:
    def __init__(self, Sender, port, parent):
        self.parent = parent
        self.Sender = Sender
        self.port = port
        self.setupUI()

    def setupUI(self):
        receivers_list_window = ReceiversListWindow()
        sender = SenderTest(self.parent, self.Sender, receivers_list_window, self.port)
        sender.show_receivers_list(receivers_list_window)


class SenderTest(UIHandlerBase):
    def __init__(self, parent, Sender, receivers_list_window, port):
        self.port = port
        self.parent = parent

        out = self.choose_file()
        if out is not None:
            path, name = out
        else:
            sys.exit()

        if path and name:
            self.sender = Sender(path, name, receivers_list_window)

            self.timer = QTimer(self.parent)
            self.timer.timeout.connect(lambda: self.window_refresh(receivers_list_window.list_widget))
            self.timer.start(1000)
            self.parent.close()

            self.progress_bar = None

    def choose_file(self):
        file_dialog = Q.QFileDialog(self.parent)
        file_dialog.setWindowTitle("Select a file: ")
        file_dialog.setFileMode(Q.QFileDialog.FileMode.ExistingFile)
        if file_dialog.exec() == Q.QFileDialog.DialogCode.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            file_info = file_dialog.selectedFiles()[0]
            file_name = file_info.split("/")[-1]
            return file_path, file_name

    def window_refresh(self, list_widget):
        """
        Constantly refresh the page and show the newest receivers
        """
        receiver_name, receiver_ip = self.sender.update_receivers_list()
        if receiver_name is not None:
            display_entry = receiver_name
            if display_entry not in [list_widget.item(i).text() for i in range(list_widget.count())]:
                item = Q.QListWidgetItem(receiver_name)
                list_widget.addItem(item)

        for i in range(list_widget.count()):
            item = list_widget.item(i)
            if item.text() not in self.sender.receivers.keys():
                list_widget.takeItem(i)

    def show_receivers_list(self, receivers_list_window):
        receivers_list_window.show()
        receivers_list_window.list_widget.itemClicked.connect(self.select_and_send)

    def select_and_send(self, item):
        receiver_name = item.text()
        func = threading.Thread(target=self.sender.connect_to_receiver, args=(self.sender.receivers[receiver_name], self.port))
        func.start()


class ReceiversListWindow(Q.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Receivers List")
        self.setGeometry(500, 200, 300, 400)
        self.list_widget = Q.QListWidget(self)
        self.progress_bar = Q.QProgressBar()
        self.progress_bar.hide()
        layout = Q.QVBoxLayout(self)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.progress_bar)

    def download_mode(self):
        self.list_widget.hide()
        self.setFixedHeight(200)
        self.setFixedWidth(500)
        self.progress_bar.show()

    def close_window(self):
        print("closed the window ")
        self.destroy()
        sys.exit()
