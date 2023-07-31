from . import constants, utils

import threading

class MessageHandler(threading.Thread):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection

    def start(self):
        self.running = True
        super().start()

    def stop(self):
        self.running = False

        try:
            utils.send(self.connection, "quit", sender="default")
        finally:
            self.join()

    def send(self, message):
        utils.send(self.connection, "global_message", sender="default", message=message)

    def run(self):
        while self.running:
            try:
                metadata = utils.receive(self.connection)
                message = metadata.message if metadata else ""

                if message and hasattr(self, "callback"):
                    self.callback(message)

            except Exception as e:
                print("Broken connection: ", self.connection)
                self.stop()

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