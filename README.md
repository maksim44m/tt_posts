# Telegram-бот для блога с API-админкой

Telegram-бот для показа постов блога с веб-административной панелью для управления постами.

## Описание функционала

### Telegram-бот
- Команда `/posts` - показывает кнопки с заголовками постов
- При нажатии на заголовок показывает текст поста и дату создания

### API-админка
- Создание/удаление/изменение постов через REST API
- Веб-интерфейс для управления постами
- Автоматическая документация API (Swagger/ReDoc)
- Авторизация для доступа к админке

## Технические требования

- Python 3.9+
- PostgreSQL
- Docker

## Быстрый запуск с Docker Compose

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd tt_posts
```

2. Создайте файл `.env` на основе `env.example`:
```bash
cp env.example .env
```

3. Отредактируйте `.env` файл:
   - Укажите токен Telegram-бота в `TG_TOKEN`
   - При необходимости измените другие настройки

4. Запустите все сервисы:
```bash
docker compose up -d
```

5. Примените миграции базы данных:
```bash
docker compose exec api alembic upgrade head
```

После запуска:
- API будет доступно по адресу: http://localhost:8002
- Документация API: http://localhost:8002/docs
- Telegram-бот будет готов к работе

## Структура проекта

```
├── api/                   # FastAPI приложение
│   ├── api_v1/            # API v1
│   ├── db/                # Модели базы данных
│   ├── services/          # Бизнес-логика
│   ├── schemas/           # Pydantic схемы
│   ├── templates/         # HTML шаблоны
│   ├── static/            # Статические файлы
│   ├── alembic/           # Миграции базы данных
│   └── requirements.txt   # Зависимости API
├── bot/                   # Telegram бот
│   ├── handlers.py        # Обработчики команд
│   ├── db.py              # Работа с базой данных
│   └── requirements.txt   # Зависимости бота
├── docker-compose.yml     # Docker Compose конфигурация
├── env.example            # Пример переменных окружения
└── README.md              # Документация
```
 