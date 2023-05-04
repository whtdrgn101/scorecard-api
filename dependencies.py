from db.config import async_session
from db.dals.user_dal import UserDAL
from db.dals.bow_dal import BowDAL
from db.dals.round_dal import RoundDAL
from db.dals.end_dal import EndDAL

async def get_user_dal():
    async with async_session() as session:
        async with session.begin():
            yield UserDAL(session)

async def get_bow_dal():
    async with async_session() as session:
        async with session.begin():
            yield BowDAL(session)

async def get_round_dal():
    async with async_session() as session:
        async with session.begin():
            yield RoundDAL(session)

async def get_end_dal():
    async with async_session() as session:
        async with session.begin():
            yield EndDAL(session)