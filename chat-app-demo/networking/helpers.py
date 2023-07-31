from . import constants

def pad(header, length=constants.HEADER_LENGTH) -> str:
    return header.ljust(length)

def join(*args):
    return constants.DATA_SEPERATOR.join(map(str, args))

def encode(header, message = "") -> bytes:
    return bytes(pad(join(header, len(message))) + message, constants.FORMAT)