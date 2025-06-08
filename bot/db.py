from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker,
                                    AsyncSession)
from sqlalchemy import MetaData, Table, Column, Integer, String, Text, DateTime, select
from sqlalchemy.sql import func

import config


class DB:
    def __init__(self):
        self.engine = create_async_engine(config.DB_URL,
                                          echo=True,
                                          future=True)
        self.Session = async_sessionmaker(bind=self.engine,
                                          expire_on_commit=False)  # данными можно пользоваться после комита

        self.metadata = MetaData()

        self.posts = Table(
            'posts',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('title', String(255), nullable=False),
            Column('content', Text, nullable=False),
            Column('created_at',
                   DateTime(timezone=True),
                   server_default=func.now(),
                   nullable=False)
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.Session() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                raise e

    async def get_posts(self, session: AsyncSession) -> list[dict]:
        """Получение списка всех постов"""
        query = select(self.posts)
        result = await session.execute(query)
        return [dict(row._mapping) for row in result]

    async def get_post(self, session: AsyncSession, post_id: int) -> dict | None:
        """Получение поста по ID"""
        query = select(self.posts).where(self.posts.c.id == post_id)
        result = await session.execute(query)
        row = result.first()
        return dict(row._mapping) if row else None
