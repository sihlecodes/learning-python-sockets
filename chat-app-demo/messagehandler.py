import constants
import utils
import threading

class MessageHandler(threading.Thread):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection

    def start(self):
        self.running = True
        super().start()
    
    def stop(self):
        self.running = False
        self.join()

    def run(self):
        while self.running:
            try:
                message = self.connection.recv(1024).decode(constants.FORMAT)

                if message and hasattr(self, "callback"):
                    self.callback(message)

            except Exception as e:
                print("Broken connection: ", self.connection)
                break

if __name__ == "__main__":
    import socket
    import time

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((constants.ADDRESS, constants.PORT))

    handler = MessageHandler(connection)

    handler.callback = lambda x: print(x)
    handler.start()

    time.sleep(10)

    handler.stop()