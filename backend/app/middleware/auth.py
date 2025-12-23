from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from sqlalchemy import select

from app.auth.telegram import verify_init_data
from app.db.session import Session
from app.db.models.user import User


class TelegramAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not request.url.path.startswith("/api"):
            return await call_next(request)

        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("tma "):
            return Response(status_code=401)

        tg_user = verify_init_data(auth[4:])

        async with Session() as session:
            result = await session.execute(
                select(User).where(User.telegram_id == tg_user.id)
            )
            user = result.scalar_one_or_none()

            if not user:
                user = User(
                    telegram_id=tg_user.id,
                    username=tg_user.username,
                )
                session.add(user)
                await session.commit()
                await session.refresh(user)

        request.state.user = user
        return await call_next(request)
