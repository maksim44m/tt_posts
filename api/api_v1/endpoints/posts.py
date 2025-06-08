from fastapi import APIRouter, Depends, Response, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.post import PostCreate, PostResponse, PostUpdate
from api_v1.dependencies import get_db_session, get_post_service
from services.posts import PostService


router = APIRouter()
templates = Jinja2Templates(directory="templates")


# API endpoints для работы с постами
@router.get('/', response_model=list[PostResponse])
async def get_posts_api(
    session: AsyncSession = Depends(get_db_session),
    post_service: PostService = Depends(get_post_service)
):
    """Получение списка всех постов"""
    return await post_service.get_posts(session)


@router.get('/{post_id}', response_model=PostResponse)
async def get_post_api(
    post_id: int,
    session: AsyncSession = Depends(get_db_session),
    post_service: PostService = Depends(get_post_service)
):
    """Получение поста по ID"""
    return await post_service.get_post(session, post_id)


@router.post('/', response_model=PostResponse, status_code=201)
async def create_post_api(
    post_data: PostCreate,
    session: AsyncSession = Depends(get_db_session),
    post_service: PostService = Depends(get_post_service)
):
    """Создание нового поста"""
    return await post_service.create_post(session, post_data)


@router.put('/{post_id}', response_model=PostResponse)
async def update_post_api(
    post_id: int,
    post_data: PostUpdate,
    session: AsyncSession = Depends(get_db_session),
    post_service: PostService = Depends(get_post_service)
):
    """Полное обновление поста"""
    return await post_service.patch_post(session, post_id, post_data)


@router.patch('/{post_id}', response_model=PostResponse)
async def patch_post_api(
    post_id: int,
    post_data: PostUpdate,
    session: AsyncSession = Depends(get_db_session),
    post_service: PostService = Depends(get_post_service)
):
    """Частичное обновление поста"""
    return await post_service.patch_post(session, post_id, post_data)


@router.delete('/{post_id}', status_code=204)
async def delete_post_api(
    post_id: int,
    session: AsyncSession = Depends(get_db_session),
    post_service: PostService = Depends(get_post_service)
):
    """Удаление поста"""
    await post_service.delete_post(session, post_id)
    return Response(status_code=204)

