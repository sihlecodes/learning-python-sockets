import socket
import pickle
import time

from threading import Thread

# TODO: decide on how client emits should be handled compared to server emits

class ESSocket:
    __timeout = 100
    __encoding = "utf-8"
    __chunk_size = 2048

    def __init__(self, *args, **kwargs):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__event_handlers = {}
        self.__is_alive = True
        self.__message_thread = Thread(target=self.__handle_incoming_messaages)
        self.__message_thread.start()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, trace):
        self.close()

    def _register_event(self, event: str, *args, **kwargs):
        self.__handle_event(event, *args, **kwargs)

    def _register_event_handler(self, event: str, event_handler: function):
        self.__event_handlers[event] = event_handler

    def emit(self, event: str, *args: list, **kwargs: dict):
        self.socket.send(pickle.dumps([event, args, kwargs]).encode(ESSocket.__encoding))

    def on(self, event: str, event_handler: function):
        self._register_event_handler(event, event_handler)

    def close():
        pass

    def __handle_event(self, event, *args, **kwargs):
        if event in self.__event_handlers:
            self.__event_handlers[event](*args, **kwargs)

    def __handle_incoming_messaages(self, client: socket.socket):
        # TODO: handle complete reading
        while self.__is_alive:
            data = client.recv(self.__chunk_size)
            break

class ESServer(ESSocket):
    def _emit_self(self, event: str, *args: list, **kwargs: dict):
        self._register_event(event, *args, **kwargs)

    def emit_on(self, client: socket.socket, event: str, *args: list, **kwargs: dict):
        data = pickle.dumps([event, args, kwargs])
        client.send(data)

class ESClient(ESSocket):
    pass