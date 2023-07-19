import socket
import constants

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((constants.ADDRESS, constants.PORT))

try:
    server.listen()
    connection, address = server.accept()

    print(address)
    print(connection)

    connection.send(b"Hello world!")

finally:
    connection.close()
    server.close()    