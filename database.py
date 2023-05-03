import os
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = sa.engine.URL.create(
        drivername="postgresql",
        username=os.environ.get('SCORECARD_USER'),
        password=os.environ.get('SCORECARD_PASS'),
        host=os.environ.get('SCORECARD_HOST'),
        database="scorecard_db",
    )

SEARCH_PATH='ols' # Searches left-to-right

engine = create_engine( DB_URL, 
    connect_args={'options': '-csearch_path={}'.format(SEARCH_PATH)})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)