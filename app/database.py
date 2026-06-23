from sqlalchemy.ext.asyncio import create_async_engine 
from sqlalchemy.orm import declarative_base , sessionmaker
from config import setting

# Create Engine.
engine = create_async_engine(url=setting.DATABASE_URL)

# Used to Create a Database.
SessionLocal = sessionmaker(bind=engine)

# Create a Table in a Main Database.
Base = declarative_base()

# Global Database Call.
async def get_database():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()