from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import DBUser
from schemas.user import UserCreate
from utils import security
import config


class UserService:
    async def register(self,
                       session: AsyncSession,
                       user: UserCreate) -> RedirectResponse:
        """Регистрация нового пользователя"""
        db_user = DBUser(
            username=user.username,
            password=security.hash_password(user.password)
        )
        query = select(DBUser).where(DBUser.username == db_user.username)
        result = await session.execute(query)
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(status_code=400,
                                detail='User already exists')
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        access_token = security.create_access_token(db_user.username)
        return await self._access_response(access_token)

    async def login(self,
                    session: AsyncSession,
                    user: UserCreate) -> RedirectResponse:
        """Аутентификация пользователя"""
        query = select(DBUser).where(DBUser.username == user.username)
        result = await session.execute(query)
        db_user = result.scalar_one_or_none()
        if (not db_user
                or not security.verify_password(user.password, db_user.password)):
            raise HTTPException(
                status_code=401, detail='Incorrect username or password')
        access_token = security.create_access_token(db_user.username)
        return await self._access_response(access_token)
    
    async def _access_response(self,
                              access_token: str) -> RedirectResponse:
        response = RedirectResponse(url='/api/v1/posts', status_code=302)
        response.set_cookie(
            key="Authorization",
            value=f"Bearer {access_token}",
            httponly=True,
            secure=config.secure,
            max_age=config.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            samesite="lax"
        )
        return response