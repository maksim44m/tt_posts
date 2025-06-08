from fastapi import APIRouter

from api_v1.endpoints import users, posts, web


routers = APIRouter()
routers.include_router(users.router, prefix="/users", tags=["users"])
routers.include_router(posts.router, prefix="/posts", tags=["posts"])
routers.include_router(web.router, prefix="/web", tags=["web"])

