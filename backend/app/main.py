from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.tasks import router as tasks_router
from app.middleware.auth import TelegramAuthMiddleware

app = FastAPI()

app.add_middleware(TelegramAuthMiddleware)

app.include_router(health_router, prefix="/api/health", tags=["health"])
app.include_router(tasks_router, prefix="/api/tasks", tags=["tasks"])
