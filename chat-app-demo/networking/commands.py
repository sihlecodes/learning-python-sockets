from .helpers import encode, join

def _message(sender, message) -> bytes:
    return encode(join("m", sender), message)

def _direct_message(sender, receiver, message) -> bytes:
    return encode(join("dm", sender, receiver), message)

def _quit(sender) -> bytes:
    return encode(join("q", sender))

_commands = {
    "global_message": _message,
    "direct_message": _direct_message,
    "quit": _quit
}

def get(command):
    return _commands.get(command)