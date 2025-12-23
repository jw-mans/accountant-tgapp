from fastapi import FastAPI
from fastapi.middleware import Middleware
from app.api import tasks
from app.middleware.auth import TelegramAuthMiddleware


app = FastAPI(middleware=[
    Middleware(TelegramAuthMiddleware)
])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])