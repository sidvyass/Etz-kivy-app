# gui/login_window.py
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from controllers.user_login_controller import LoginController
import asyncio
from controllers.base_logger import getlogger


KV = """
<LoginWindow>:
    name: 'login_screen'
    MDFloatLayout:
        # Set the background color to dark
        canvas.before:
            Color:
                rgba: 0.1, 0.1, 0.1, 1  # Dark background
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
                size_hint: None, None
                size: dp(280), dp(48)  # Fixed size
                pos_hint: {"center_x": 0.5}
                line_color_normal: 1, 1, 1, 1  # White line color
                text_color: 1, 1, 1, 1  # White text color
                hint_text_color_normal: 0.7, 0.7, 0.7, 1  # Light grey hint text

            MDTextField:
                id: password_field
                hint_text: "Password"
                password: True
                size_hint: None, None
                size: dp(280), dp(48)  # Fixed size
                pos_hint: {"center_x": 0.5}
                line_color_normal: 1, 1, 1, 1  # White line color
                text_color: 1, 1, 1, 1  # White text color
                hint_text_color_normal: 0.7, 0.7, 0.7, 1  # Light grey hint text

            MDRaisedButton:
                text: "Login"
                size_hint: None, None
                size: dp(140), dp(48)  # Fixed size
                pos_hint: {"center_x": 0.5}
                md_bg_color: 0.2, 0.2, 0.2, 1  # Dark button background
                text_color: 1, 1, 1, 1  # White text color
                on_release: root.start_login()

        MDSpinner:
            id: loading_spinner
            size_hint: None, None
            size: dp(46), dp(46)
            pos_hint: {"center_x": 0.5, "center_y": 0.3}
            active: False
            color: 1, 1, 1, 1  # White spinner color
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
        await self.controller.authenticate(
            self.ids.username_field.text, self.ids.password_field.text
        )
        self.ids.loading_spinner.active = False

    def show_password(self):
        password_field = self.ids.password_field
        # Toggle the password visibility
        if password_field.password:
            password_field.password = False
            password_field.icon_right = (
                "eye"  # Change to "eye" icon to indicate password is visible
            )
        else:
            password_field.password = True
            password_field.icon_right = "eye-off"
