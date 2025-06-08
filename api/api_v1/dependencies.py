from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from db.base import DB
from services.users import UserService
from services.posts import PostService


# Singletons
_db_instance: DB | None = None


def get_db_instance() -> DB:
    """Получение singleton экземпляра базы данных"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DB()
    return _db_instance


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency для получения сессии базы данных"""
    db = get_db_instance()
    async for session in db.get_session():
        yield session


def get_user_service() -> UserService:
    """Dependency для получения экземпляра UserService"""
    return UserService()


def get_post_service() -> PostService:
    """Dependency для получения экземпляра PostService"""
    return PostService()