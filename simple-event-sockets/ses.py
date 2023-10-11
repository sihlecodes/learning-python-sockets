import socket
import pickle
import time

from threading import Thread

# TODO: decide on how client emits should be handled compared to server emits

class ESSocket:
    __timeout = 100
    __encoding = "utf-8"
    __chunk_size = 2048

    def __init__(self, host, port, *args, **kwargs):
        self.host = host
        self.port = port
        self.verbose = kwargs.get('verbose', False)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.__event_handlers = {}
        self.__is_alive = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, trace):
        self.close()

    def _register_event_handler(self, event: str, event_handler: callable):
        self.__event_handlers[event] = event_handler

    def emit(self, event: str, *args: list, **kwargs: dict):
        data = pickle.dumps([event, args, kwargs])
        self.socket.send(data.encode(ESSocket.__encoding))

    def on(self, event: str, event_handler: callable):
        self._register_event_handler(event, event_handler)

    def close(self):
        self.__is_alive = False
        self.socket.close()

    def __handle_event(self, event, *args, **kwargs):
        has_event_handler = event in self.__event_handlers

        if has_event_handler:
            self.__event_handlers[event](*args, **kwargs)
        else:
            print(f"Event handler for '{event}' is not defined.")

        # return has_event_handler

    def __handle_incoming_messaages(self, client: socket.socket):
        # TODO: test
        while self.__is_alive:
            data = client.recv(self.__chunk_size)

            try:
                data = pickle.loads(data)

                if len(data) == 3:
                    event, args, kwargs = data
                    self.__handle_event(event, *args, **kwargs)

            except pickle.UnpicklingError:
                continue

class ESServer(ESSocket):
    def __init__(self, host, port):
        super().__init__(host, port)

        self.socket.bind((host, port))
        Thread(target=self.__handle_connections).start()

    def _emit_self(self, event: str, *args: list, **kwargs: dict):
        self._register_event(event, *args, **kwargs)

    def emit_on(self, client: socket.socket, event: str, *args: list, **kwargs: dict):
        data = pickle.dumps([event, args, kwargs])
        client.send(data.encode(ESServer.__encoding))

    def __handle_connections(self, server: socket.socket):
        threads = []

        while self.__is_alive:
            server.listen()

            client, _ = server.accept()

            thread = Thread(target=self.__handle_incoming_messaages, args=(client,))
            thread.start()

            threads.append(thread)

class ESClient(ESSocket):
    def __init__(self, host, port):
        super().__init__(host, port)

        self.socket.connect((host, port))
        Thread(target=self.__handle_incoming_messaages, args=(self.socket,)).start()