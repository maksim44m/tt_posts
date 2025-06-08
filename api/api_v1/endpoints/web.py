from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.post import PostCreate, PostUpdate
from api_v1.dependencies import get_db_session, get_post_service
from services.posts import PostService

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/', include_in_schema=False)
async def posts_page(
    request: Request,
    session: AsyncSession = Depends(get_db_session),
    post_service: PostService = Depends(get_post_service)
):
    """Страница со списком постов"""
    posts = await post_service.get_posts(session)
    return templates.TemplateResponse(
        "posts.html", 
        {"request": request, "posts": posts}
    )


@router.get('/new', include_in_schema=False)
async def new_post_page(request: Request):
    """Страница создания нового поста"""
    return templates.TemplateResponse(
        "post_form.html", 
        {"request": request}
    )


@router.post('/new', include_in_schema=False)
async def create_web_post(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    session: AsyncSession = Depends(get_db_session),
    post_service: PostService = Depends(get_post_service)
):
    """Создание нового поста через веб-интерфейс"""
    try:
        post_data = PostCreate(title=title, content=content)
        await post_service.create_post(session, post_data)
        response = RedirectResponse(
            url="/api/v1/posts?success=Пост успешно создан", 
            status_code=302
        )
        return response
    except Exception as e:
        return templates.TemplateResponse(
            "post_form.html", 
            {
                "request": request, 
                "error": str(e)
            }
        )


@router.get('/{post_id}/edit', include_in_schema=False)
async def edit_post_page(
    request: Request,
    post_id: int,
    session: AsyncSession = Depends(get_db_session),
    post_service: PostService = Depends(get_post_service)
):
    """Страница редактирования поста"""
    try:
        post = await post_service.get_post(session, post_id)
        return templates.TemplateResponse(
            "post_form.html", 
            {"request": request, "post": post}
        )
    except HTTPException as e:
        return RedirectResponse(
            url=f"/api/v1/posts?error={e.detail}", 
            status_code=302
        )


@router.post('/{post_id}/edit', include_in_schema=False)
async def update_web_post(
    request: Request,
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    session: AsyncSession = Depends(get_db_session),
    post_service: PostService = Depends(get_post_service)
):
    """Обновление существующего поста через веб-интерфейс"""
    try:
        post_data = PostUpdate(title=title, content=content)
        await post_service.patch_post(session, post_id, post_data)
        response = RedirectResponse(
            url="/api/v1/posts?success=Пост успешно обновлен", 
            status_code=302
        )
        return response
    except HTTPException as e:
        return RedirectResponse(
            url=f"/api/v1/posts?error={e.detail}", 
            status_code=302
        )
    except Exception as e:
        post = await post_service.get_post(session, post_id)
        return templates.TemplateResponse(
            "post_form.html", 
            {
                "request": request, 
                "post": post, 
                "error": str(e)
            }
        )


@router.post('/{post_id}/delete', include_in_schema=False)
async def delete_web_post(
    post_id: int,
    session: AsyncSession = Depends(get_db_session),
    post_service: PostService = Depends(get_post_service)
):
    """Удаление поста через веб-интерфейс"""
    try:
        await post_service.delete_post(session, post_id)
        return RedirectResponse(
            url="/api/v1/posts?success=Пост успешно удален", 
            status_code=302
        )
    except HTTPException as e:
        return RedirectResponse(
            url=f"/api/v1/posts?error={e.detail}", 
            status_code=302
        )