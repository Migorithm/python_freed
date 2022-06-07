from typing import Any
from sqlalchemy import inspect
from sqlalchemy.orm import as_declarative
from sqlalchemy.orm.session import sessionmaker

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseSettings

class Settings(BaseSettings):
    STAGE:str = "testing"
    #POSTGRES
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: str 
    POSTGRES_SERVER: str
    POSTGRES_PORT: str 
    POSTGRES_DB:str
 

settings = Settings(_env_file='../../postgres.env')

class DBConfig:
    def __init__(self):
        self.engine = create_async_engine(self.postgres_url(),pool_pre_ping=False,echo=True)
        self.async_session = sessionmaker(
                self.engine, 
                class_=AsyncSession, 
                expire_on_commit=False
                )

    def postgres_url(self):
        url = "postgresql+asyncpg://{}:{}@{}:{}/{}"
        if settings.STAGE == "testing":
            POSTGRES_DB = settings.POSTGRES_DB + "_test"
        else: 
            POSTGRES_DB = settings.POSTGRES_DB
        return url.format(
                    settings.POSTGRES_USER, 
                    settings.POSTGRES_PASSWORD, 
                    settings.POSTGRES_SERVER, 
                    settings.POSTGRES_PORT, 
                    POSTGRES_DB, 
            )

    async def get_session(self) -> AsyncSession:
        async with self.async_session() as session:
            yield session

    async def init_models(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)



@as_declarative()
class Base:
    id: Any
    __name__: str

    def _to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


db = DBConfig()