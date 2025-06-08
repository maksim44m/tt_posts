from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from db import DB


_db_instance: DB | None = None


def get_db_instance() -> DB:
    """Получение singleton экземпляра базы данных"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DB()
    return _db_instance
