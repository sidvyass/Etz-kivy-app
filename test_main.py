import asyncio
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.app import MDApp
from controllers.user_controller import UserAPI
from gui.email_window.email_window_main import EmailTrackerWindow
from controllers.email_controller.main_email_controller import EmailTrackerController
from gui.email_window.loading_screen import LoadingScreen
from gui.email_window.edit_info_popup import EditInfoPopup


class EsisAutoApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Ghostwhite"

        self.screen_manager = ScreenManager(transition=NoTransition())
        Window.size = (1200, 900)

        self.loading_screen = LoadingScreen()
        self.screen_manager.add_widget(self.loading_screen)

        self.email_controller = EmailTrackerController(
            self, UserAPI("60009", "67220"), self.loading_screen
        )
        self.email_tracker_view = EmailTrackerWindow(controller=self.email_controller)
        self.screen_manager.add_widget(self.email_tracker_view)

        return self.screen_manager


if __name__ == "__main__":
    asyncio.run(EsisAutoApp().async_run(async_lib="asyncio"))
