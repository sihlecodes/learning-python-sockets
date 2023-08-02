from . import constants, utils
from .commands import Commands

import threading
import random

class MessageHandler(threading.Thread):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.username = f"user{random.randint(1000, 10000)}"

        utils.send(connection, Commands.SIGN_IN, self.username)

    def start(self):
        self.running = True
        super().start()

    def stop(self):
        self.running = False
        utils.send(self.connection, Commands.QUIT, self.username)

    def send(self, message):
        utils.send(self.connection, Commands.GLOBAL_MESSAGE, self.username, message=message)

    def run(self):
        while self.running:
            try:
                metadata = utils.receive(self.connection)
            except OSError:
                break

            if not metadata:
                continue

            message = metadata.message
            sender = metadata.parameters[0]

            if message and hasattr(self, "callback"):
                self.callback(sender, message)

if __name__ == "__main__":
    import socket
    import time

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((constants.ADDRESS, constants.PORT))

    handler = MessageHandler(connection)

    handler.callback = lambda x: print(x)
    handler.start()

    time.sleep(10)

    handler.stop()