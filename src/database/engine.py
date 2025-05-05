from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from backend.config import DatabaseSetting
from database.models import Base


db = DatabaseSetting()

db_url = f"postgresql+asyncpg://{db.db_username}:{db.db_password}@{db.db_host}:{db.db_port}/{db.db_name}"

async_engine = create_async_engine(db_url, pool_pre_ping=True, pool_recycle=300)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False
)


async def create_tables(engine = async_engine):
    """Создание таблиц"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables(engine = async_engine):
    """Удаление таблиц"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_db_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
