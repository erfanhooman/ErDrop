import tkinter as tk
from tkinter import filedialog
import sys
from sender.userInter_faces.GUIBase import UIHandlerBase


class GUIHandler(UIHandlerBase):
    """
    handler of the UI
    """
    def __init__(self, Sender, port, parent):
        """
        to do call the three essential method and other method
        """
        path, name = self.choose_file()
        self.port = port
        self.window = tk.Tk()
        self.window.title("Receivers")
        self.listbox = tk.Listbox(self.window)
        self.listbox.pack()
        self.svr = Sender(path, name)
        self.window.after(0, self.window_refresh)
        self.listbox.bind('<Double-1>', self.select_and_send)
        self.window.mainloop()

    def choose_file(self):
        """
        choose the file method , the function that ask for the file path
        :return: tuple of : name, filepath
        """
        root = tk.Tk()
        root.withdraw()

        filepath = filedialog.askopenfilename(title="Choose a file you want to send")
        if filepath is None:
            sys.exit()
        filename = filepath.split('/')[-1]
        return filepath, filename

    def select_and_send(self, event):
        """
        select the user and send the file to it
        """
        if self.listbox.size() > 0:
            receiver_name = self.listbox.get(self.listbox.curselection())
            if receiver_name in self.svr.receivers:
                self.svr.connect_to_receiver(self.svr.receivers[receiver_name], self.port)
                self.svr.end_discovering()
                self.window.destroy()
            else:
                self.listbox.delete(self.listbox.get(0, tk.END).index(receiver_name))
        else:
            print("Receiver Not Found")

    def window_refresh(self):
        """
        constantly refresh the page and show the newest receivers
        """
        receiver_name, receiver_ip = self.svr.update_receivers_list()
        if receiver_name is not None:
            display_entry = receiver_name
            if display_entry not in self.listbox.get(0, tk.END):
                self.listbox.insert(tk.END, receiver_name)

        for item in self.listbox.get(0, tk.END):
            if item not in self.svr.receivers.keys():
                self.listbox.delete(self.listbox.get(0, tk.END).index(item))

        self.window.after(500, self.window_refresh)
