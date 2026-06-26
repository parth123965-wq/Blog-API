import asyncio
import sys
from pathlib import Path
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from sqlalchemy.future import select

from app.database import engine, Base, SessionLocal
from app.models.post_M import Category


async def create_tables():
    print("Connecting to Render PostgreSQL and creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        for name, description in [
            ("General", "General blog posts"),
            ("Technology", "Technology related posts"),
            ("Lifestyle", "Lifestyle and personal posts"),
        ]:
            existing = await session.execute(select(Category).where(Category.category_name == name))
            if existing.scalar_one_or_none() is None:
                session.add(Category(category_name=name, description=description))
        await session.commit()

    print("🎉 All database tables created successfully inside Render!")


if __name__ == "__main__":
    asyncio.run(create_tables())