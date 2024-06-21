import asyncpg
from app.config import settings

async def get_db_pool():
    return await asyncpg.create_pool(settings.DATABASE_URL)

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await get_db_pool()

    async def disconnect(self):
        await self.pool.close()

database = Database()
