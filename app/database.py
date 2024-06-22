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

    async def init_db(self):
        async with self.pool.acquire() as conn:
            await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                middle_name VARCHAR(100),
                sex VARCHAR(1),
                city VARCHAR(100),
                phone VARCHAR(15) UNIQUE,
                email VARCHAR(100) UNIQUE,
                pass_hash VARCHAR(100),
                temp_pass_hash VARCHAR(100),
                user_type VARCHAR(100),
                whatsapp VARCHAR(50),
                telegram VARCHAR(50),
                viber VARCHAR(50),
                zoom VARCHAR(50),
                prop_city VARCHAR(100),
                prop_offer VARCHAR(100),
                prop_type VARCHAR(100),
                prop_state VARCHAR(100),
                avatar VARCHAR(100) DEFAULT 'noUserImage.svg',
                licenses VARCHAR(100) DEFAULT 'noLicenseImage.svg',
                video VARCHAR(100) DEFAULT 'noVideo.svg',
                about VARCHAR(500),
                activation_code VARCHAR(10),
                role VARCHAR(10) DEFAULT 'user',
                updated BIGINT
            )''')

database = Database()
