from fastapi import HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.post import PostCreate, PostUpdate
from db.models import DBPost


class PostService:
    async def create_post(self,
                          session: AsyncSession,
                          post: PostCreate) -> DBPost:
        db_post = DBPost(title=post.title, content=post.content)
        session.add(db_post)
        await session.commit()
        await session.refresh(db_post)
        return db_post

    async def get_posts(self,
                        session: AsyncSession) -> list[DBPost]:
        query = select(DBPost)
        result = await session.execute(query)
        db_posts = result.scalars().all()
        return db_posts

    async def get_post(self,
                       session: AsyncSession,
                       post_id: int) -> DBPost:
        query = select(DBPost).where(DBPost.id == post_id)
        result = await session.execute(query)
        db_post = result.scalar_one_or_none()
        if not db_post:
            raise HTTPException(status_code=404, detail="Post not found")
        return db_post

    async def patch_post(self,
                         session: AsyncSession,
                         post_id: int,
                         post: PostUpdate) -> DBPost:
        query = select(DBPost).where(DBPost.id == post_id)
        result = await session.execute(query)
        db_post = result.scalar_one_or_none()
        if not db_post:
            raise HTTPException(status_code=404, detail="Post not found")
        for field, value in post.model_dump().items():
            if value is not None:
                setattr(db_post, field, value)
        await session.commit()
        await session.refresh(db_post)
        return db_post

    async def delete_post(self,
                          session: AsyncSession,
                          post_id: int) -> Response:
        query = select(DBPost).where(DBPost.id == post_id)
        result = await session.execute(query)
        db_post = result.scalar_one_or_none()
        if not db_post:
            raise HTTPException(status_code=404, detail="Post not found")
        session.delete(db_post)
        await session.commit()
        return Response(status_code=204)

