from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api_v1.endpoints.routers import routers
from api_v1.middlewares import AuthMiddleware, LoggingMiddleware


app = FastAPI(
    title="Posts API",
    description="Cервер для работы с постами блога через API",
    version="0.1.0"
)

# Шаблоны для веб-интерфейса
templates = Jinja2Templates(directory="templates")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware в правильном порядке (последний добавленный выполняется первым)
app.add_middleware(AuthMiddleware)  # Выполняется вторым
app.add_middleware(LoggingMiddleware)  # Выполняется первым

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")

# Редирект с корневого URL
@app.get("/")
async def root():
    """Редирект на страницу логина"""
    return RedirectResponse(url="/api/v1/users/login", status_code=302)

# API роуты
app.include_router(routers, prefix="/api/v1")
