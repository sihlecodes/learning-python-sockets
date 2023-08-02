from networking import utils, constants
from networking.commands import Commands

import socket
import threading

class MessageDelegater:
    def __init__(self):
        self.client_handlers = {}

    def add(self, sender, client_handler):
        self.client_handlers[sender] = client_handler

    def remove(self, target):
        self.client_handlers.pop(target)

    def send_all(self, sender, message):
        for client_handler in self.client_handlers.values():
            utils.send(client_handler.connection, Commands.MESSAGE, sender, message)

    def send(self, sender, receiver, message):
        reciepient_handler = self.client_handlers[receiver]

        utils.send(reciepient_handler, Commands.MESSAGE, sender, message)

class ClientHandler(threading.Thread):
    def __init__(self, client, message_delegater):
        super().__init__()
        self.connection, self.address = client
        self.username = self.address
        self.message_delegater = message_delegater

    def _handle_request(self, metadata):
        if not metadata:
            return

        sender = metadata.parameters[0]
        print(metadata)

        match metadata.command:
            case Commands.GLOBAL_MESSAGE:
                self.message_delegater.send_all(sender, metadata.message)

            case Commands.DIRECT_MESSAGE:
                sender, receiver = metadata.parameters
                self.message_delegater.send(sender, receiver, metadata.message)

            case Commands.QUIT:
                self.connection.close()
                self.message_delegater.remove(sender)
                self.stop()

            case Commands.SIGN_IN:
                self.username = sender
                self.message_delegater.add(sender, self)

    def start(self):
        self.running = True
        super().start()

    def stop(self):
        self.running = False
        self.join()

    def run(self):
        print("[NEW CONNECTION]:", self.address)

        with self.connection:
            while self.running:
                metadata = utils.receive(self.connection)
                self._handle_request(metadata)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((constants.ADDRESS, constants.PORT))

client_handlers: list = []

message_delegater = MessageDelegater()

try:
    server.listen()

    while True:
        client: tuple = server.accept()

        handler = ClientHandler(client, message_delegater)
        handler.start()

        client_handlers.append(handler)

finally:
    server.close()

    for handler in client_handlers:
        handler.stop()