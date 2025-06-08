from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserCreate, UserResponse
from api_v1.dependencies import get_db_session, get_user_service
from services.users import UserService


router = APIRouter()
templates = Jinja2Templates(directory="templates")




# Маршруты для авторизации
@router.get('/login', include_in_schema=False)
async def login_page(request: Request):
    """Страница входа"""
    return templates.TemplateResponse("login.html", {"request": request})


@router.post('/login', include_in_schema=False)
async def login_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(get_db_session),
    user_service: UserService = Depends(get_user_service)
):
    """Аутентификация пользователя через веб-интерфейс"""
    try:
        user_data = UserCreate(username=username, password=password)
        return await user_service.login(session, user_data)
    except HTTPException as e:
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, "error": e.detail}
        )


@router.get('/register', include_in_schema=False)
async def register_page(request: Request):
    """Страница регистрации"""
    return templates.TemplateResponse("register.html", {"request": request})


@router.post('/register', include_in_schema=False)
async def register_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(get_db_session),
    user_service: UserService = Depends(get_user_service)
):
    """Регистрация нового пользователя через веб-интерфейс"""
    try:
        user_data = UserCreate(username=username, password=password)
        return await user_service.register(session, user_data)
    except HTTPException as e:
        return templates.TemplateResponse(
            "register.html", 
            {"request": request, "error": e.detail}
        )


@router.get('/logout', include_in_schema=False)
async def logout_user():
    """Выход пользователя"""
    response = RedirectResponse(url="/api/v1/users/login", status_code=302)
    response.delete_cookie(key="Authorization")
    return response
