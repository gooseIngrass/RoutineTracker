from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = 'sqlite+aiosqlite:///db.sqlite3'

engine = create_async_engine(url=DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
