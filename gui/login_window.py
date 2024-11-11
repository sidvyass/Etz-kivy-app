from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

# from controllers.login_controller import LoginController


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
                size_hint: None, None
                size: dp(280), dp(48)  # Fixed size
                pos_hint: {"center_x": 0.5}
                text_color: 1, 1, 1, 1  # White text color

                MDTextFieldHintText:
                    text: "User ID. Ex: 36154"

            MDTextField:
                id: password_field
                password: True
                size_hint: None, None
                size: dp(280), dp(48)  # Fixed size
                pos_hint: {"center_x": 0.5}
                text_color: 1, 1, 1, 1  # White text color

                MDTextFieldHintText:
                    text: "Password"

            MDButton:
                id: search_button
                style: "filled"
                on_release: root.controller.authenticate(root.ids.username_field.text, root.ids.password_field.text, root)
                size: dp(140), dp(48)  # Fixed size
                pos_hint: {"center_x": 0.5}
                theme_bg_color: "Custom"
                md_bg_color: 0.2, 0.2, 0.2, 1  # Dark button background

                MDButtonText:
                    id: search_button_text
                    text: "Login"
                    theme_text_color: "Custom"
                    text_color: "white"
"""
# NOTE: the controller calls the load_main_window function once auth is successful


class LoginWindow(Screen):
    controller = ObjectProperty()

    def __init__(self, controller, **kwargs):
        super(LoginWindow, self).__init__(**kwargs)
        self.controller = controller

    def on_enter(self, *args):
        Clock.schedule_once(self.controller.check_server_status)
        super().on_enter(*args)

    def on_leave(self, *args):
        super().on_leave(*args)


Builder.load_string(KV)
