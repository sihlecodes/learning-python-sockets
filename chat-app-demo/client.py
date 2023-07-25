from collections.abc import Callable, Iterable, Mapping
from typing import Any
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ListProperty

import socket
import constants
import random
import utils
import threading


class CustomLabel(Label):
    pass

class MessageHandler(threading.Thread):
    def __init__(self, connection, messages, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = connection
        self.messages = messages

    def run(self):
        while True:
            try:
                message = self.connection.recv(1024).decode(constants.FORMAT)

                if message:
                    self.messages.append(message)
            finally:
                break
            # except Exception as e:
            #     raise e
            #     print("Broken connection: ", self.connection)
            #     break

class ClientUI(BoxLayout):
    messages = ListProperty([])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.connection = connection

        layout = self.ids.message_container
        layout.bind(minimum_height = layout.setter("height"))

    def on_messages(self, instance, messages):
        label = CustomLabel(text=messages[-1])
        self.ids.message_container.add_widget(label)

class ClientApp(App):
    def __init__(self, connection, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = ClientUI()
        self.message_handler = MessageHandler(connection, self.ui.messages)

    def build(self):
        return self.ui

if __name__ == '__main__':
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((constants.ADDRESS, constants.PORT))

    try:
        app = ClientApp(connection)
        app.run()
    finally:
        connection.close()