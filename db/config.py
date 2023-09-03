import os
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = sa.engine.URL.create(
        drivername="postgresql",
        username=os.environ.get('SCORECARD_USER'),
        password=os.environ.get('SCORECARD_PASS'),
        host=os.environ.get('SCORECARD_HOST'),
        database=os.environ.get('SCORECARD_DB'),
    )

engine = sa.create_engine(DATABASE_URL)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()