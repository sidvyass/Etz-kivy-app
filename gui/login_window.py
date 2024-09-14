# gui/login_window.py

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from controllers.user_login_controller import LoginController
import asyncio
from base_logger import getlogger

KV = """
<LoginWindow>:
    name: 'login_screen'
    MDFloatLayout:
        # Set the background color to white
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1  # White background
            Rectangle:
                pos: self.pos
                size: self.size

        MDBoxLayout:
            orientation: 'vertical'
            size_hint: None, None
            size: dp(320), dp(200)  # Adjust the size as needed
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            padding: dp(20)
            spacing: dp(15)

            MDTextField:
                id: username_field
                hint_text: "Username"
                icon_right: "account"
                size_hint: None, None
                size: dp(280), dp(48)  # Fixed size
                pos_hint: {"center_x": 0.5}

            MDTextField:
                id: password_field
                hint_text: "Password"
                icon_right: "eye-off"
                password: True
                size_hint: None, None
                size: dp(280), dp(48)  # Fixed size
                pos_hint: {"center_x": 0.5}

            MDRaisedButton:
                text: "Login"
                size_hint: None, None
                size: dp(140), dp(48)  # Fixed size
                pos_hint: {"center_x": 0.5}
                on_release: root.start_login()

        MDSpinner:
            id: loading_spinner
            size_hint: None, None
            size: dp(46), dp(46)
            pos_hint: {"center_x": 0.5, "center_y": 0.3}
            active: False
"""

Builder.load_string(KV)


class LoginWindow(Screen):
    controller = ObjectProperty()

    def __init__(self, controller, **kwargs):
        super(LoginWindow, self).__init__(**kwargs)
        self.controller: LoginController = controller
        self.LOGGER = getlogger("Login GUI")

    def hide_spinner(self):
        self.ids.loading_spinner.active = False

    def start_login(self):
        asyncio.create_task(self.login())

    async def login(self):
        self.ids.loading_spinner.active = True
        bool_value = await self.controller.authenticate(
            self.ids.username_field.text, self.ids.password_field.text
        )
        self.ids.loading_spinner.active = False
        if bool_value == False:
            # TODO: change this to false and render a box upon incorrect attempt
            pass
