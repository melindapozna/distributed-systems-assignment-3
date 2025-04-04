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


if __name__ == "__main__":
    thread = threading.Thread(target=receive)
    thread.start()

    print("Type /q to quit")
    nickname = input("Enter your nickname:")
    if nickname == "/q":
        print("Goodbye!")
        exit(0)

    while True:
        message = input()
        if message == "/q":
            print("Goodbye!")
            exit(0)
        client.sendto(f"{nickname}: {message}".encode(), ("localhost", 6000))

