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


class CustomLabel(Label):
    pass

class ClientUI(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = self.ids.message_container
        layout.bind(minimum_height = layout.setter("height"))

    def _on_new_message(self, message):
        Clock.schedule_once(lambda x: self.add_message(message))
    
    def add_message(self, message):
        label = CustomLabel(text=message)
        self.ids.message_container.add_widget(label)

class ClientApp(App):
    def __init__(self, connection, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_handler = MessageHandler(connection)

    def _on_request_close(self, *args):
        self.message_handler.stop()

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