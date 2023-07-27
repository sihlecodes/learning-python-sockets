import socket
import threading
import constants
import utils
import time

class ClientHandler(threading.Thread):
    def __init__(self, client, clients):
        super().__init__()
        self.connection, self.address = client
        self.clients = clients

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
                self.connection.send(b"Hello, world!")
                time.sleep(3)

                # message: str = utils.get_message(self.connection)

                # for client_connection, client_address in self.clients:
                #     try:
                #         if client_connection != self.connection:
                #             client_connection.send(b"Hello, world!")#utils.encode(message))

                #     except:
                #         self.clients.remove(client)
                #         print("[REMOVED CLIENT]:", client)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((constants.ADDRESS, constants.PORT))

client_handlers: list = []
clients: list = []

try:
    server.listen()

    while True:
        client: tuple = server.accept()
        clients.append(client)

        handler = ClientHandler(client, clients)
        handler.start()

        client_handlers.append(handler)

finally:
    server.close()
    
    for handler in client_handlers:
        handler.stop()