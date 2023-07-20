import socket
import threading
import constants

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((constants.ADDRESS, constants.PORT))

def handle_client(connection, address):
    while True:
        length: int = int(connection.recv(constants.HEADER_LENGTH))
        message: str = connection.recv(length).decode()

        print(f"[{address}]:", message)

try:
    server.listen()

    while True:
        client: tuple = server.accept()

        thread = threading.Thread(target=handle_client, args=client)
        thread.start()


finally:
    server.close()