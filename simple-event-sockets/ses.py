import socket
import pickle
import time

from threading import Thread

# TODO: decide on how client emits should be handled compared to server emits
# TODO: make __clients retry connections on each __timeout until program calls .close()

class ESSocket:
    __encoding = "utf-8"
    __chunk_size = 2048

    def __init__(self, host, port, **kwargs):
        self.host = host
        self.port = port
        self.verbose = kwargs.get('verbose', False)
        self.timeout = kwargs.get('timeout', 100)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.__event_handlers = {}
        self.__is_alive = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, trace):
        pass
        # self.close()

    def _register_event_handler(self, event: str, event_handler: callable):
        self.__event_handlers[event] = event_handler

    def emit(self, event: str, *args: list, **kwargs: dict):
        data = pickle.dumps([event, args, kwargs])
        self.socket.send(data)

    def on(self, event: str, event_handler: callable):
        self._register_event_handler(event, event_handler)

    def is_alive(self):
        return self.__is_alive

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

    def _handle_incoming_messaages(self, client: socket.socket):
        while self.__is_alive:
            try:
                data = client.recv(ESSocket.__chunk_size)
                data = pickle.loads(data)

                if len(data) == 3:
                    event, args, kwargs = data
                    self.__handle_event(event, *args, **kwargs)

            except pickle.UnpicklingError:
                continue

            except ConnectionResetError:
                break

class ESServer(ESSocket):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.__clients = []
        self.socket.bind((host, port))

        Thread(target=self._handle_connections, args=(self.socket,)).start()

    def _emit_self(self, event: str, *args: list, **kwargs: dict):
        self._register_event(event, *args, **kwargs)

    def emit_on(self, client: socket.socket, event: str, *args: list, **kwargs: dict):
        data = pickle.dumps([event, args, kwargs])
        client.send(data.encode(ESServer.__encoding))

    def emit(self, event: str, *args: list, **kwargs: dict):
        for client in self.__clients:
            self.emit_on(client, event, *args, **kwargs)

    def _handle_connections(self, server: socket.socket):
        threads = []

        while self.is_alive():
            server.listen()

            client, _ = server.accept()
            self.__clients.append(client)
            print("client connected")

            thread = Thread(target=self._handle_incoming_messaages, args=(client,))
            thread.start()

            threads.append(thread)

class ESClient(ESSocket):
    def __init__(self, host, port):
        super().__init__(host, port)

        self._establish_connection(host, port)
        Thread(target=self._handle_incoming_messaages, args=(self.socket,)).start()

    def _establish_connection(self, host, port):
        try:
            self.socket.connect((host, port))
            print("connection established")
        except ConnectionRefusedError:
            if self.is_alive():
                print("connection failed, trying again")
                time.sleep(self.timeout)
                self._establish_connection(host, port)