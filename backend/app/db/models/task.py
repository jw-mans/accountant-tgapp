from sqlalchemy import (
    ForeignKey, String, func, Integer,
    DateTime
)
from sqlalchemy.orm import (
    Mapped, mapped_column, relationship
)
from app.db.base import Base
from datetime import datetime

class Task(Base):
    __tablename__ = 'tasks'

    id:          Mapped[       int] = mapped_column(Integer,
                                                    primary_key=True, 
                                                    index=True)
    title:       Mapped[       str] = mapped_column(String(255), 
                                                    nullable=False)
    description: Mapped[str | None] = mapped_column(String(1023))
    status:      Mapped[       str] = mapped_column(String(63), 
                                                    nullable=False, 
                                                    default='pending')

    user_id:     Mapped[       int] = mapped_column(ForeignKey('users.id'), 
                                                    nullable=False)
    created_at:  Mapped[  datetime] = mapped_column(DateTime(timezone=True),
                                                    server_default=func.now(), 
                                                    nullable=False)

    user = relationship('User', back_populates='tasks')