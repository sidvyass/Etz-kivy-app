import asyncio
import aioodbc
from base_logger import getlogger


class MainWindowModel:
    def __init__(self):
        self.LOGGER = getlogger("Main Model")

        self.connection_string = (
            "DRIVER={SQL Server};SERVER=ETZ-SQL;DATABASE=SANDBOX;Trusted_Connection=yes"
        )

    async def fetch_document_data(self):
        pass
