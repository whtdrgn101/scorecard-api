import os
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = sa.engine.URL.create(
        drivername="postgresql+asyncpg",
        username=os.environ.get('SCORECARD_USER'),
        password=os.environ.get('SCORECARD_PASS'),
        host=os.environ.get('SCORECARD_HOST'),
        database="scorecard_db",
    )

engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, autoflush=True, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()