import socket
import threading
import constants
import utils
import time

def handle_client(connection, address, clients):
    print("[NEW CONNECTION]:", address)

    while True:
        connection.send(b"Hello, world!")
        time.sleep(3)

        # message: str = utils.get_message(connection)

        # for client in clients:
        #     if client != connection:
        #         client.send(utils.encode(message))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((constants.ADDRESS, constants.PORT))

threads: list = []
clients: list = []

try:
    server.listen()

    while True:
        client: tuple = server.accept()
        clients.append(client[0])

        thread = threading.Thread(target=handle_client, args=(*client, clients))
        thread.start()

        threads.append(thread)

finally:
    server.close()
    
    # for thread in threads:
    #     thread.join()