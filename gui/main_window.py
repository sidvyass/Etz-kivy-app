# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from navbar import NavBar
# from table_display import DisplayDocs


# class MyApp(App):
#     def build(self):
#         main_layout = BoxLayout(orientation="vertical")
#
#         nav_section = NavBar(size_hint=(1, 0.2))
#         display_doc = DisplayDocs(size_hint=(1, 0.8))
#
#         main_layout.add_widget(nav_section)
#         main_layout.add_widget(display_doc)
#
#         return main_layout


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from controllers.user_login_controller import LoginController
import asyncio


class LoginWindow(BoxLayout):
    """The view (UI) for the login window."""

    def __init__(self, controller, **kwargs):
        super(LoginWindow, self).__init__(**kwargs)
        self.controller = controller
        self.orientation = "vertical"

        # Username Input
        self.add_widget(Label(text="Username"))
        self.username_input = TextInput(multiline=False)
        self.add_widget(self.username_input)

        # Password Input
        self.add_widget(Label(text="Password"))
        self.password_input = TextInput(multiline=False, password=True)
        self.add_widget(self.password_input)

        # Login Button
        self.login_button = Button(text="Login")
        self.login_button.bind(on_press=self.on_login_button_press)
        self.add_widget(self.login_button)

        # Placeholder for message button
        self.message_button = None

    def on_login_button_press(self, instance):
        """Delegate the login action to the controller."""
        username = self.username_input.text
        password = self.password_input.text
        self.show_loading_icon()
        asyncio.create_task(self.controller.start_login(self.show_message))

    def show_loading_icon(self):
        self.loading_icon = None
        if not self.loading_icon:
            self.loading_icon = Label(text="Loading...", size_hint=(1, 0.2))
            self.add_widget(self.loading_icon)

    def show_message(self, message):
        """Display a message in the view."""
        if self.loading_icon is not None:
            self.remove_widget(self.loading_icon)

        # Create a button with the message
        self.message_button = Button(text=message, size_hint=(1, 0.2))
        self.add_widget(self.message_button)
