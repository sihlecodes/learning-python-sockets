import constants

def encode(message: str) -> bytes:
    return bytes(f"{len(message):<{constants.HEADER_LENGTH}}{message}", constants.FORMAT)

def get_message(connection) -> str:
    length: int = int(connection.recv(constants.HEADER_LENGTH))
    message: str = connection.recv(length).decode(constants.FORMAT)

    return message