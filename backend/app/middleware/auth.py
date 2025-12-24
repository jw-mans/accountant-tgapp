from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse
from sqlalchemy import select

from app.auth.telegram import verify_init_data
from app.db.session import Session
from app.db.models.user import User


class TelegramAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ['/health', '/health/']:
            return await call_next(request)

        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("tma "):
            return JSONResponse(
                status_code=401,
                content={
                    'detail': "Wrong Authorization header"
                }
            )
        try:
            tg_user = verify_init_data(auth[4:])
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    'detail': exc.detail
                }
            )
        except Exception as ex:
            return JSONResponse(
                status_code=500,
                content={
                    'detail': 'Internal authentifaction error'
                }
            )

        async with Session() as session:
            result = await session.execute(
                select(User).where(
                    User.telegram_id == tg_user.id
                )
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
