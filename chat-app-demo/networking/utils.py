from . import commands, constants

class Metadata:
    def __init__(self, command, parameters, message):
        self.command = command
        self.parameters = parameters
        self.message = message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.command}, {self.parameters}, {self.message})"

def send(connection, command, *args, **kwargs) -> bytes | None:
    if not command:
        raise Exception("No command specified")

    data: bytes = commands.get(command)(*args, **kwargs)

    try:
        connection.send(data)
    except BrokenPipeError:
        return

    return data

def receive(connection) -> Metadata:
    header: str = connection.recv(constants.HEADER_LENGTH).decode(constants.FORMAT).strip()
    print(header)

    if not header:
        return

    parameters: list = header.split(constants.DATA_SEPERATOR)

    if len(header) > 0 and len(parameters) < 2:
        raise Exception("Bad data format")

    command: str = parameters.pop(0)
    length:  int = int(parameters.pop())
    message: str = connection.recv(length).decode(constants.FORMAT)

    return Metadata(command, parameters, message)

# if __name__ == "__main__":
#     print(send(None, "global_message", "steve", message="Hello, Everyone!"))
#     print(send(None, "direct_message", "steve", message="Hello, John!", receiver="john"))
#     print(send(None, "quit", "steve"))