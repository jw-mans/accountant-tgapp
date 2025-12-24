from sqlalchemy import (
    BigInteger, func, DateTime
)
from sqlalchemy.orm import (
    Mapped, mapped_column, relationship
)
from app.db.base import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id:             Mapped[       int] = mapped_column(BigInteger, 
                                                       primary_key=True, 
                                                       index=True,
                                                       autoincrement=True)
    telegram_id:    Mapped[       int] = mapped_column(BigInteger, 
                                                       unique=True, 
                                                       index=True, 
                                                       nullable=False)
    username:       Mapped[str | None]
    created_at:     Mapped[  datetime] = mapped_column(DateTime(timezone=True), 
                                                       server_default=func.now(), 
                                                       nullable=False)

    tasks = relationship('Task', 
                         back_populates='user',
                         cascade='all, delete')