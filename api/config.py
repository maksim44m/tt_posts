import os
from typing import Optional

from dotenv import load_dotenv


load_dotenv()

def get_env_var(name: str, default: Optional[str] = None) -> str:
    """Получение переменной окружения с проверкой"""
    value = os.getenv(name, default)
    if value is None or value.strip() == '':
        raise ValueError(f'Переменная окружения {name} не установлена')
    return value

# Настройки безопасности куки
secure = False

# Настройки путей, которые не требуют авторизации
PUBLIC_PATHS = [
    "/",
    "/api/v1/users/login",
    "/api/v1/users/register", 
    "/api/v1/posts/api/",
    "/api/v1/posts/api",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/static",
]

# Настройки JWT
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

# Переменные окружения
SECRET_KEY: str = get_env_var('SECRET_KEY')
DB_URL: str = get_env_var('DB_URL')

# Настройки API
API_HOST: str = get_env_var('API_HOST', '0.0.0.0')
API_PORT: int = int(get_env_var('API_PORT', '8002'))

