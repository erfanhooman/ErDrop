import sys, os

from sender.choosefile.ChooseFIleBase import ChooseFileBase

from tkinter import Tk, filedialog


class TkinterFileChooser(ChooseFileBase):
    def pathfinder(self):
        root = Tk()
        root.withdraw()

        filepath = filedialog.askopenfilename(title="Choose a file")
        if filepath is None:
            sys.exit()
        filename = filepath.split('/')[-1]
        return filepath, filename


class SendPathManually(ChooseFileBase):
    def pathfinder(self):
        while True:
            path = input("Enter the file path manually: ")

            if not os.path.exists(path):
                print("Error: The specified path does not exist.")
                continue

            if not os.path.isfile(path):
                print("Error: The specified path does not point to a file.")
                continue

            break
        filename = os.path.basename(path)

        return path, filename