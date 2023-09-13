import socket
import pickle
import time

from threading import Thread

# TODO: decide on how client emits should be handled compared to server emits

class ESSocket:
    __timeout = 100
    __encoding = "utf-8"

    def __init__(self, *args, **kwargs):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__events = []
        self.__event_handlers = {}
        self.__is_alive = True
        self.__message_thread = Thread(target=self.__handle_incoming_messaages)
        self.__message_thread.start()

        # TODO: decide whether this second thread should exist or not
        self.__event_thread = Thread(target=self.__handle_events)
        self.__event_thread.start()

    def _register_event(self, event: str, *args, **kwargs):
        self.__events.append(event)

    def _register_event_handler(self, event: str, event_handler: function):
        self.__event_handlers[event] = event_handler

    def emit(self, event: str, *args: list, **kwargs: dict):
        self.socket.send(pickle.dumps([event, args, kwargs]).encode(ESSocket.__encoding))

    def on(self, event: str, event_handler: function):
        self._register_event_handler(event, event_handler)

    def __handle_events(self):
        while self.__is_alive:
            if len(self.__events) == 0:
                time.sleep(ESSocket.__timeout)
                continue

            event, args, kwargs = self.__events.pop(0)

            if event in self.__event_handlers:
                self.__event_handlers[event](*args, **kwargs)


    def __handle_incoming_messaages(self, client: socket.socket):
        # TODO: handle client messages
        pass

class ESServer(ESSocket):
    def _emit_self(self, event: str, *args: list, **kwargs: dict):
        self._register_event(self, event, *args, **kwargs)

    def emit_on(self, client: socket.socket, event: str, *args: list, **kwargs: dict):
        data = pickle.dumps([event, args, kwargs])
        client.send(data)

class ESClient(ESSocket):
    pass