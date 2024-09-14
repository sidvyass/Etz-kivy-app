import asyncio
import aioodbc
from base_logger import getlogger


class UserAuthentication:
    def __init__(self):
        self.LOGGER = getlogger("User Auth")

        self.connection_string = (
            "DRIVER={SQL Server};SERVER=ETZ-SQL;DATABASE=SANDBOX;Trusted_Connection=yes"
        )

    async def fetch_user_data(self) -> list:
        self.LOGGER.info("Fetching user data...")
        async with await aioodbc.connect(dsn=self.connection_string) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT Code, Password FROM [user]")
                data = await cursor.fetchall()
                self.LOGGER.info("user data fetched")
                if len(data) > 0:
                    return data
                else:
                    return []
