import threading
import socket
import queue
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer

# list of online clients
clients = []
nicknames_to_addresses = {}
nicknames_to_addresses.setdefault("", "")

groups = {}

private_messages = queue.Queue()
group_messages = queue.Queue()

# init UDP socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 6000))


def receive(client):
    try:
        message, address = server.recvfrom(2048)
        message_attributes = message.decode().split("::")
        nickname = message_attributes[0]
        content = message_attributes[1]
        message_type = message_attributes[2]    # g - group, p - private
        recipient = message_attributes[3]

        if address not in clients:
            clients.append(address)

        if message_type == "p":
            private_messages.put((nickname, content, nicknames_to_addresses[recipient], address))
            if not nickname in nicknames_to_addresses:
                nicknames_to_addresses[nickname] = address

        elif message_type == "g":
            group_messages.put((nickname, content, groups[recipient], address))
            if not groups[recipient]:
                groups[recipient] = [address]
            if address not in groups[recipient]:
                groups[recipient].append(address)
        print(message)
    except:
        pass
        # TODO


def send_private():
    while True:
        while not private_messages.empty():
            nickname, content, recipient, address = private_messages.get()
            try:
                if address not in clients:
                    pass
                server.sendto(f"{nickname}: {content}".encode(), nicknames_to_addresses[recipient])
            except:
                clients.remove(nicknames_to_addresses[recipient])
                nicknames_to_addresses.pop(recipient)

def send_group():
    while True:
        while not group_messages.empty():
            nickname, content, group_name, address = private_messages.get()
            try:
                if address not in clients:
                    pass
                for address in groups[group_name]:
                    server.sendto(f"{group_name.upper()}/{nickname}: {content}".encode(), address)
            except:
                groups[group_name].remove(address)


thread_receive = threading.Thread(target=receive)
thread_private = threading.Thread(target=send_private)
thread_group = threading.Thread(target=send_group)

thread_receive.start()
thread_private.start()
thread_group.start()
