import socket
from threading import Thread

class ESSocket:
    def emit(self, event: str):
        pass

    def on(self, event: str):
        pass

class ESServer(ESSocket):
    pass

class ESClient(ESSocket):
    pass