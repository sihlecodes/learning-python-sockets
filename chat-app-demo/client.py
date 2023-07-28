from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window

import socket
import constants
import random
import utils
import time
import threading

from messagehandler import MessageHandler

class CustomLabel(Label):
    pass

class ClientUI(BoxLayout):
    def _on_new_message(self, message):
        print("new message")
        messages = self.ids.messages
        messages.text += f"\n{message}" if messages.text else message

class ClientApp(App):
    def __init__(self, connection, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_handler = MessageHandler(connection)

    def _on_request_close(self, *args):
        self.message_handler.stop()

    def send(self, message):
        self.message_handler.send(message)

    def build(self):
        ui = ClientUI()

        self.message_handler.callback = ui._on_new_message
        self.message_handler.start()

        Window.bind(on_request_close=self._on_request_close)
        return ui 

if __name__ == '__main__':
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((constants.ADDRESS, constants.PORT))

    try:
        app = ClientApp(connection)
        app.run()
    finally:
        connection.close()