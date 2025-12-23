from fastapi import HTTPException, status
from aiogram.utils.web_app import check_webapp_signature, parse_webapp_init_data
from app.config import TG_BOT_TOKEN


def verify_init_data(init_data: str):
    try:
        check_webapp_signature(
            token=TG_BOT_TOKEN,
            init_data=init_data,
        )
        data = parse_webapp_init_data(init_data)

        if not data.user:
            raise ValueError

        return data.user

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Telegram initData",
        )
