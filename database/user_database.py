import asyncio
import aioodbc


class UserAuthentication:
    def __init__(self):
        self.connection_string = (
            "DRIVER={SQL Server};SERVER=ETZ-SQL;DATABASE=SANDBOX;Trusted_Connection=yes"
        )

    async def fetch_single_user(self):
        async with await aioodbc.connect(dsn=self.connection_string) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT * FROM Item")
                await cursor.fetchall()
                print("this function finished")

    async def fetch_inventory(self):
        async with await aioodbc.connect(dsn=self.connection_string) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT * FROM Item where ItemPK=1")
                val = await cursor.fetchall()
                print(val)

    async def main(self):
        task1 = asyncio.create_task(u.fetch_single_user())
        task2 = asyncio.create_task(u.fetch_inventory())

        await task1
        await task2


if __name__ == "__main__":
    u = UserAuthentication()
    asyncio.run(u.main())
