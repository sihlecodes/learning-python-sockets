from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import socket
import constants
import random
import utils
import time
import threading

from messagehandler import MessageHandler

class CustomTextInput(TextInput):
    def _grab_focus(self, *args):
        self.focus = True

    def grab_focus(self):
        Clock.schedule_once(self._grab_focus)

    def clear(self):
        self.text = ""

class ClientUI(BoxLayout):
    def _on_enter_pressed(self, *args):
        self.ids.send.trigger_action(0.1)

    def _on_send_pressed(self, message):
        app = App.get_running_app()
        app.send(message)

        self.ids.new_message.clear()
        self.ids.new_message.grab_focus()

    def _on_new_message(self, message):
        messages = self.ids.messages
        messages.text += f"\n{message}" if messages.text else message

class ClientApp(App):
    def __init__(self, connection, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = "Chat App Demo"
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