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


DB_URL: str = get_env_var('DB_URL')
TG_TOKEN: str = get_env_var('TG_TOKEN')