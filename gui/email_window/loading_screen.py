from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from controllers.base_logger import getlogger

LOGGER = getlogger("loading screen")


KV = """
<LoadingScreen>:
    name: 'loading_screen_email_app'

    MDScreen:
        md_bg_color: self.theme_cls.backgroundColor

        MDLabel:
            halign: "center"
            id: update_text
            text: "Building your configs..."

        MDLinearProgressIndicator:
            id: progress
            size_hint_x: .5
            value: 0
            type: "determinate"
            pos_hint: {'center_x': .5, 'center_y': .4}

"""


class LoadingScreen(Screen):
    def __init__(self, **kwargs) -> None:
        super(LoadingScreen, self).__init__(**kwargs)
        self.progress = 0

    def on_enter(self, *args):
        self.progress = 0
        return super().on_enter(*args)

    def update_progress(
        self, val=0, update_text="Hold on while we read your emails..."
    ):
        """Update progress bar incrementally."""

        if self.progress < 100:
            self.progress += val
            self.ids.progress.value = self.progress
            self.ids.update_text.text = update_text
        else:
            LOGGER.info("Loading complete.")

    def on_loading_complete(self):
        pass


Builder.load_string(KV)
