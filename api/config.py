import os
from dotenv import load_dotenv

load_dotenv()


# Настройки безопасности куки
secure = False

# Настройки путей, которые не требуют авторизации
PUBLIC_PATHS = [
    "/",
    "/api/v1/users/login",
    "/api/v1/users/register", 
    "/api/v1/posts/",
    "/api/v1/posts",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/static",
]

# Настройки JWT
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

# Переменные окружения
SECRET_KEY: str = os.getenv('SECRET_KEY')
DB_URL: str = os.getenv('DB_URL')

# Настройки API
API_HOST: str = os.getenv('API_HOST', '0.0.0.0')
API_PORT: int = int(os.getenv('API_PORT', '8002'))

