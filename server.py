import threading
import socket
import queue

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


def receive():
    while True:
        try:
            message, address = server.recvfrom(2048)
            message_attributes = message.decode().split("::")
            nickname = message_attributes[0]
            content = message_attributes[1]
            message_type = message_attributes[2]    # g - group, p - private
            recipient = message_attributes[3]

            if address not in clients:
                print("address added:", address)
                clients.append(address)

            if message_type == "p":
                if nickname not in nicknames_to_addresses:
                    nicknames_to_addresses[nickname] = address

                private_messages.put((nickname, content, recipient, address))

            elif message_type == "g":
                group_messages.put((nickname, content, recipient, address))
                if recipient not in groups:
                    groups[recipient] = [address]
                if address not in groups[recipient]:
                    groups[recipient].append(address)
            print(message)
        except Exception as e:
            print(e)
            continue


def send_private():
    while True:
        while not private_messages.empty():
            nickname, content, recipient_nickname, sender_address = private_messages.get()
            try:
                if recipient_nickname not in nicknames_to_addresses:
                    print(f"Recipient {recipient_nickname} not found.")
                    continue
                recipient_address = nicknames_to_addresses[recipient_nickname]
                server.sendto(f"[PRIVATE] {nickname}: {content}".encode(), recipient_address)

            except:
                clients.remove(sender_address)
                nicknames_to_addresses.pop(nickname)



def send_group():
    while True:
        while not group_messages.empty():
            nickname, content, group_name, address = group_messages.get()
            try:
                if address not in clients:
                    continue
                for member_address in groups[group_name]:
                    server.sendto(f"{group_name.upper()}/{nickname}: {content}".encode(), member_address)
            except:
                groups[group_name].remove(address)


thread_receive = threading.Thread(target=receive)
thread_private = threading.Thread(target=send_private)
thread_group = threading.Thread(target=send_group)

thread_receive.start()
thread_private.start()
thread_group.start()
