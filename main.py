import sys

from sender.sender import UIHandler
from receiver.receiver import Receiver


def run_sender():
    print("Running sender.py")
    UIHandler()


def run_receiver():
    print("Running receiver.py")
    Receiver().start_server()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py [sender|receiver]")
    else:
        option = sys.argv[1]
        if option == "sender":
            run_sender()
        elif option == "receiver":
            run_receiver()
        else:
            print("Invalid option. Use 'sender' or 'receiver'.")
