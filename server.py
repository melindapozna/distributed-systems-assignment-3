import threading
import socket
import queue

# list of online clients
clients = []

messages = queue.Queue()

# init UDP socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 6000))


def receive():
    try:
        messages.put(server.recvfrom(2048))
    except:
        pass
        # TODO


# send to every client
def broadcast():
    while True:
        while not messages.empty():
            message, address = messages.get()
            print(message.decode())
            if address not in clients:
                clients.append(address)
            for client in clients:
                try:
                    if message.decode().startswith("nickname:"):
                        nickname = message.decode()[message.decode().index(":") + 1:]
                        server.sendto(f"{nickname} joined!".encode(), client)
                    else:
                        server.sendto(message, client)
                except:
                    clients.remove(client)


thread1 = threading.Thread(target=receive)
thread2 = threading.Thread(target=broadcast)

thread1.start()
thread2.start()
