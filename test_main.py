# import sys
# import os
#
# if getattr(sys, "frozen", False):
#     # Running in PyInstaller bundle
#     base_path = sys._MEIPASS
# else:
#     # Running in normal Python environment
#     base_path = os.path.dirname(os.path.abspath(__file__))
#
# # Ensure the project root is on sys.path
# project_root = os.path.dirname(os.path.abspath(__file__))
# if project_root not in sys.path:
#     sys.path.append(project_root)
#
#
import asyncio
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.app import MDApp
from controllers.user_controller import UserAPI
from gui.email_window.email_window_main import EmailTrackerWindow
from controllers.email_controller.main_email_controller import EmailTrackerController
from gui.email_window.loading_screen import LoadingScreen
from gui.email_window.edit_info_popup import EditInfoPopup
from gui.email_window.inbox_picker import open_dropdown_dialog

from controllers.email_controller.main_email_controller import (
    get_email_reply_gpt_response,
)


class EsisAutoApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Ghostwhite"

        self.screen_manager = ScreenManager(transition=NoTransition())
        Window.size = (1200, 900)

        self.loading_screen = LoadingScreen()
        self.screen_manager.add_widget(self.loading_screen)

        self.email_controller = EmailTrackerController(self, self.loading_screen)
        self.email_tracker_view = EmailTrackerWindow(controller=self.email_controller)
        self.screen_manager.add_widget(self.email_tracker_view)

        return self.screen_manager


if __name__ == "__main__":
    asyncio.run(EsisAutoApp().async_run(async_lib="asyncio"))
