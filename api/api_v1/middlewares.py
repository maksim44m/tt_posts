import time
from typing import Callable

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

import config
from utils import security
from utils.log import logging


logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()
        
        # Логирование входящего запроса
        logger.info(f'Запрос: {request.method} {request.url.path}')
        
        try:
            response = await call_next(request)
            
            process_time = time.time() - start_time
            
            # Логирование ответа с временем обработки
            logger.info(f'Ответ: {response.status_code} за {process_time:.4f}с')
            
            return response
            
        except HTTPException as e:
            process_time = time.time() - start_time
            logger.error(f'Ошибка при обработке запроса: {e.status_code}: {e.detail} за {process_time:.4f}с')
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        # Проверка публичных путей
        path = request.url.path
        
        # Проверка точного соответствия
        if path in config.PUBLIC_PATHS:
            return await call_next(request)
        
        # Проверка путей, которые начинаются с публичного префикса
        for public_path in config.PUBLIC_PATHS:
            if path.startswith(public_path + '/') or path.startswith(public_path + '?'):
                return await call_next(request)
            
        # Проверка путей с параметрами
        # Например /api/v1/posts/1 должен соответствовать шаблону /api/v1/posts/{post_id}
        for public_path in config.PUBLIC_PATHS:
            if '{' in public_path:
                # Преобразуем шаблонный путь в регулярное выражение
                import re
                pattern = public_path.replace('{', '(?P<').replace('}', '>[^/]+)')
                if re.match(f"^{pattern}$", path):
                    return await call_next(request)
        
        # Получение токена из заголовка или cookie
        bearer_token = request.headers.get("Authorization")
        if not bearer_token:
            # Попытка получить токен из cookie
            cookie_auth = request.cookies.get("Authorization")
            if cookie_auth and cookie_auth.startswith("Bearer "):
                bearer_token = cookie_auth
        
        if not bearer_token or not bearer_token.startswith("Bearer "):
            # Для веб-страниц перенаправляем на логин
            if request.headers.get("accept", "").startswith("text/html"):
                return RedirectResponse(url="/api/v1/users/login", status_code=302)
            raise HTTPException(status_code=401, 
                                detail="Missing or invalid token")

        token = bearer_token.split(" ")[1]
        user = security.verify_token(token)
        if not user:
            # Для веб-страниц перенаправляем на регистрацию
            if request.headers.get("accept", "").startswith("text/html"):
                return RedirectResponse(url="/api/v1/users/register", status_code=302)
            raise HTTPException(status_code=401, detail="Unauthorized")

        request.state.user = user
        return await call_next(request)