from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from src.core.config import settings


class DataBase:
    def __init__(self, db_url: str) -> None:

        self.engine = create_async_engine(db_url)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, expire_on_commit=False
        )

    async def dispose(self):
        await self.engine.dispose()

    async def get_session(self):
        async with self.session_factory() as session:
            yield session


db_helper = DataBase(db_url=settings.db_url)


class Base(DeclarativeBase):
    pass
