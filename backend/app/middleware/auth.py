from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.db.session import Session
from app.db.models.user import User
from app.config import TG_BOT_TOKEN
from sqlalchemy.ext.asyncio import AsyncSession
import hashlib
import hmac

async def verify_telegram_init_data(init_data: str) -> int:
    """
    Verifies the Telegram WebApp initData
    """
    data_items = dict(item.split("=") for item in init_data.split("&"))
    check_string = "\n".join(f"{k}={v}" for k, v in sorted(data_items.items()) if k != "hash")
    secret_key = hashlib.sha256(TG_BOT_TOKEN.encode()).digest()
    hmac_hash = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()
    
    if hmac_hash != data_items.get("hash"):
        raise HTTPException(status_code=401, detail="Invalid Telegram initData")
    
    return data_items

class TelegramAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("tma "):
            raise HTTPException(
                status_code=401, 
                detail="Missing Authorization header"
            )
        
        init_data = auth_header[4:]
        user_data = await verify_telegram_init_data(init_data)

        async with Session() as session:
            async with session.begin():
                user = await session.get(User, int(user_data["id"]))
                if not user:
                    user = User(
                        id=int(user_data["id"]),
                        telegram_id=int(user_data["id"]),
                        username=user_data.get("username")
                    )
                    session.add(user)
        
        request.state.user = user
        return await call_next(request)