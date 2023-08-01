from .helpers import encode, join

class Commands:
    GLOBAL_MESSAGE = "m"
    DIRECT_MESSAGE = "dm"
    MESSAGE = "m" # alias for GLOBAL_MESSAGE
    SIGN_IN = "s"
    QUIT = "q"

def _message(sender, message) -> bytes:
    return encode(join("m", sender), message)

def _direct_message(sender, receiver, message) -> bytes:
    return encode(join("dm", sender, receiver), message)

def _quit(sender) -> bytes:
    return encode(join("q", sender))

def _sign_in(sender):
    return encode(join("s", sender))

_commands = {
    Commands.GLOBAL_MESSAGE: _message,
    Commands.DIRECT_MESSAGE: _direct_message,
    Commands.QUIT: _quit,
    Commands.SIGN_IN: _sign_in,
}

def get(command):
    return _commands.get(command)