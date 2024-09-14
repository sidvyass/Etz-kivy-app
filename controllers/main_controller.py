import asyncio
from base_logger import getlogger
from database.main_window_database import MainWindowModel


class MainWindowController:
    """The controller handles interactions between the view and the model."""

    def __init__(self, main_model, app):
        self.model: MainWindowModel = main_model  # type hint for auto complete
        self.LOGGER = getlogger("Main Window Controller")
        # NOTE: self.data is a coroutine object. These need to be awaited before we use the return value
        self.data = asyncio.create_task(self.model.fetch_document_data())
        self.app = app  # this is the main app by which we call mainwindow
