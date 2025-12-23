from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import DB_URL

engine = create_async_engine(DB_URL, echo=True)

Session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)