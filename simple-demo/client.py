import socket
import constants

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((constants.ADDRESS, constants.PORT))

with client:
    print(client.recv(12))