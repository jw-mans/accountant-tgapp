from aiogram.utils.web_app import check_webapp_signature, parse_webapp_init_data
from app.config import TG_BOT_TOKEN
from fastapi import HTTPException

def verify_init_data(init_data: str):
    if not init_data:
        raise HTTPException(
            status_code=401, 
            detail="Empty Telegram initData"
        )

    try:
        if not check_webapp_signature(TG_BOT_TOKEN, init_data):
            raise ValueError("Invalid signature")

        data = parse_webapp_init_data(init_data)

        if not data.user:
            raise ValueError("No user in initData")
        
        return data.user

    except Exception as e:
        raise HTTPException(
            status_code=401, 
            detail="Invalid Telegram initData"
        )