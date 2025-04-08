import threading
import socket
from random import randint


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("localhost", randint(1000, 5999)))

def receive():
    try:
        message, _ = client.recvfrom(2048)
        print(message.decode())
    except:
        pass
        # TODO

def send(nickname, recipient, message_type):
    while True:
        message = input()
        if message == "/q":
            print("Goodbye!")
            client.close()
            exit(0)
        elif message == "/change":
            recipient, message_type = change_message_type()
        else:
            client.sendto(f"{nickname}::{message}::{message_type}::{recipient}".encode(), ("localhost", 6000))


def change_message_type():
    while True:
        print("""Change message type:
    1. Private message
    2. Groups
    0. Quit
        """)
        try:
            choice = int(input("Your choice:"))
        except TypeError:
            print("Invalid choice")
            continue
        if choice == 0:
            print("Goodbye!")
            client.close()
            exit(0)
        elif choice == 1:
            return change_recipient("p")
        elif choice == 2:
            return change_recipient("g")


def change_recipient(message_type):
    recipient = input("Enter your recipient/channel:")
    if recipient == "/q":
        print("Goodbye!")
        client.close()
        exit(0)
    return recipient, message_type



if __name__ == "__main__":
    thread_rcv = threading.Thread(target=receive)
    thread_rcv.start()

    print("Type /q to quit")
    print("Type /change to change message type")

    nickname = input("Enter your nickname:")
    if nickname == "/q":
        print("Goodbye!")
        exit(0)

    change_message_type()

    thread_send = threading.Thread(target=send)
    thread_send.start()


