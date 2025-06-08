from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

import config
from db.models import Base


class DB:
    def __init__(self):
        self.engine = create_async_engine(config.DB_URL,
                                          echo=True,
                                          future=True)
        self.Session = async_sessionmaker(bind=self.engine,
                                          expire_on_commit=False)  # данными можно пользоваться после комита

        self.all_tables = Base.metadata.tables

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.Session() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                raise e

