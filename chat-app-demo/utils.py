import constants

def encode(message: str) -> bytes:
    return bytes(f"{len(message):<{constants.HEADER_LENGTH}}{message}", constants.FORMAT)

def get_message(connection) -> str:
    header: bytes = connection.recv(constants.HEADER_LENGTH)
    message: str = ""

    if header:
        length: int = int(header)
        message = connection.recv(length).decode(constants.FORMAT)

    return message