from .models import User,Book
from fastapi import FastAPI, Depends
from .freed_db import db as DB
from sqlalchemy.orm import Session,selectinload
from sqlalchemy import select
import uuid 

app = FastAPI()


@app.get("/")
async def index(db:Session = Depends(DB.get_session)):
    user = User(name ="Migo",password="Not")
    await DB.init_models()
    db.add(user)
    await db.commit()

@app.get("/users")
async def user(db:Session = Depends(DB.get_session)):
    user = await db.execute(select(User))
    user = user.all()
    print(user)
    return user

@app.post("/add_books")
async def add_books(user:str , bookname:str, db:Session = Depends(DB.get_session)):
    book = Book(name=bookname)

    #Using traditional asyncio, the application needs to avoid any points 
    #at which IO-on-attribute access may occur. Above, the following measures are taken to prevent this:
    user = await db.scalars(select(User).filter_by(name=user).options(selectinload(User.books)))
    print("dd")
    user:User = user.first()
    book.user = user
    # user.books = book
    db.add_all([book])
    
    await db.commit()
    await db.refresh(user)
    return user.books

@app.post("/add_book")
async def add_books(user:str , bookname:str, db:Session = Depends(DB.get_session)):
    book = Book(name=bookname)
    user = await db.get(select(User).filter_by(name=user).options(selectinload(User.books)))
    print("dd")
    user:User = user.first()
    book.user = user
    # user.books = book
    db.add_all([book])
    
    await db.commit()
    await db.refresh(user)
    return user.books
    
    
    