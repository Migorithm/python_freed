from .freed_db import Base
from sqlalchemy import Column, ForeignKey,String
from sqlalchemy.orm import relationship,Mapped
from sqlalchemy.dialects import postgresql
from uuid import UUID,uuid4


class User(Base):
    __tablename__ = "users"
    name:str = Column(String(32))
    password:str = Column(String(32))
    id:UUID = Column(postgresql.UUID(as_uuid=True),primary_key=True,default=uuid4)
    books:Mapped["Book"] = relationship(
        "Book", back_populates="user",cascade="all,delete-orphan"
    )


class Book(Base):
    __tablename__ = "books"
    name:str = Column(String(32))
    id:UUID = Column(postgresql.UUID(as_uuid=True),primary_key=True,default=uuid4)
    user_id:UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey(User.__tablename__+".id", ondelete="cascade")
    )
    user: Mapped["User"] = relationship(
        "User", back_populates="books"
    )


