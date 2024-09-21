from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window
from gui.home_window import HomeWindow
import asyncio

# To test the look and feel of the app or a new page.


class EsisAutoApp(MDApp):
    dialog = None

    def build(self):
        self.screen_manager = ScreenManager(transition=NoTransition())
        controller = None

        Window.size = (1200, 900)

        # ------ just change this to the new window. Use absolute imports
        view = HomeWindow(controller=controller)
        # ------ just change this to the new window. Use absolute imports

        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"

        self.screen_manager.add_widget(view)

        return self.screen_manager


if __name__ == "__main__":
    asyncio.run(EsisAutoApp().async_run(async_lib="asyncio"))
