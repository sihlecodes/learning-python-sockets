import socket
import constants

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((constants.ADDRESS, constants.PORT))

def wrap_message(message: str):
    return f"{len(message):<{constants.HEADER_LENGTH}}{message}" 

with connection:
    while True:
        message: str = input("\033[34mSend a message to the server: \033[0m")
        data: bytes = bytes(wrap_message(message), constants.FORMAT)

        connection.send(data)