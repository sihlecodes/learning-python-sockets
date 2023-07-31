from . import constants

commands = None

class Metadata:
    def __init__(self, command, options, message):
        self.command = command
        self.options = options
        self.message = message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(map(str, [self.command, self.options, self.message]))})"

def send(connection, command, *args, **kwargs) -> bytes:
    from . import commands

    if not command:
        raise Exception("No command specified")

    data: bytes = commands.get(command)(*args, **kwargs)
    connection.send(data)

    return data

def receive(connection) -> Metadata:
    header: str = connection.recv(constants.HEADER_LENGTH).decode(constants.FORMAT).strip()

    if not header:
        return

    options: list = header.split(constants.DATA_SEPERATOR)

    if len(header) > 0 and len(options) < 2:
        raise Exception("Bad data format")

    command: str = options.pop(0)
    length:  int = int(options.pop())
    message: str = connection.recv(length).decode(constants.FORMAT)

    return Metadata(command, options, message)

# if __name__ == "__main__":
#     print(send(None, "global_message", "steve", message="Hello, Everyone!"))
#     print(send(None, "direct_message", "steve", message="Hello, John!", receiver="john"))
#     print(send(None, "quit", "steve"))