from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.engine.url import URL

from src.database.models import Base

# Настройки подключения к тестовой БД PostgreSQL
DATABASE_TEST_URL = URL.create(
    drivername="postgresql+asyncpg",
    username="postgres",
    password="postgres",
    host="localhost",
    port=5432,
    database="postgres"
)


test_engine = create_async_engine(
    DATABASE_TEST_URL,
    echo=False,
    future=True
)


TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def init_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def get_test_db_session():
    async with TestSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
