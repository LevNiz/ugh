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

    async def drop_tables(self):
        async with self.pool.acquire() as conn:
            await conn.execute("DROP TABLE IF EXISTS users CASCADE")
            await conn.execute("DROP TABLE IF EXISTS properties CASCADE")

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
                role VARCHAR(15),
                updated BIGINT
            )''')

            await conn.execute('''
                CREATE TABLE IF NOT EXISTS properties (
                    id SERIAL PRIMARY KEY,
                    realtor_id INT REFERENCES users(id),
                    deal_format VARCHAR(100),
                    type VARCHAR(100),
                    subtype VARCHAR(100),
                    condition VARCHAR(100),
                    entry_year INT,
                    entry_quarter INT,
                    purpose VARCHAR(100),
                    location VARCHAR(255),
                    price DECIMAL,
                    currency VARCHAR(10),
                    title VARCHAR(255),
                    description TEXT,
                    images TEXT[],
                    floor INT,
                    total_area DECIMAL,
                    living_area DECIMAL,
                    ceiling_height DECIMAL,
                    rooms INT,
                    bedrooms INT,
                    bathrooms INT,
                    features TEXT[],
                    equipment TEXT[], 
                    layout VARCHAR(255), 
                    building_floors INT,
                    building_living_area DECIMAL,
                    apartments INT,
                    lifts_per_entrance INT,
                    building_features TEXT[],
                    building_name VARCHAR(255),
                    developer VARCHAR(255),
                    materials VARCHAR(255),
                    building_layout VARCHAR(255),
                    territory_area DECIMAL,
                    territory_features TEXT[],
                    territory_layout VARCHAR(255),
                    nearby_places TEXT[], 
                    views TEXT[],
                    video_title VARCHAR(255),
                    video_url VARCHAR(255),
                    services TEXT[],
                    commission_amount DECIMAL,
                    commission_type VARCHAR(100), 
                    documents TEXT[], 
                    document_file1 VARCHAR(255),
                    document_file2 VARCHAR(255),
                    document_file3 VARCHAR(255),                                           
                    status VARCHAR(50) DEFAULT 'available',
                    created_at INT
                );                                                              
            ''')

            await conn.execute('''
                CREATE TABLE IF NOT EXISTS requests (
                    id SERIAL PRIMARY KEY,
                    user_id INT REFERENCES users(id) ON DELETE CASCADE,
                    city VARCHAR(100) NOT NULL,
                    district VARCHAR(100),
                    deal_format VARCHAR(50) NOT NULL,
                    type VARCHAR(50) NOT NULL,
                    subtype VARCHAR(50),
                    condition VARCHAR(50),
                    construction_year INT,
                    construction_quarter INT,
                    total_rooms VARCHAR(50),
                    total_area_min FLOAT,
                    total_area_max FLOAT,
                    budget_min FLOAT,
                    budget_max FLOAT,
                    currency VARCHAR(10),
                    purchase_purpose VARCHAR(100),
                    urgency VARCHAR(50),
                    purchase_method VARCHAR(50),
                    mortgage_approved BOOLEAN,
                    wishes TEXT
                );
                               
            ''')

database = Database()
