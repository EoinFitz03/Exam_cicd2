# app/main.py
from typing import Optional

from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Response, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import engine, SessionLocal
from app.models import Base,AuthorDB, BookDB
from app.schemas import (
    AuthorCreate,AuthorRead,
    BooksCreate, BooksRead
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (dev/exam). Prefer Alembic in production.
    Base.metadata.create_all(bind=engine)
    yield
Base.metadata.create_all(bind= engine)

app = FastAPI(lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()


# ---- Health ----
@app.get("/health")
def health():
    return {"status": "ok"}

#Users

@app.get("/api/users", response_model=AuthorRead)
def list_users(db: Session = Depends(get_db)):
    stmt = select(AuthorDB).order_by(AuthorDB.id)
    result= db.execute(stmt)
    authors = result.scalars().all
    return authors

@app.get("/api/users/{author_id}", response_model=AuthorRead)
def get_author(author_id:int, db: Session = Depends(get_db)):
    author = db.get(AuthorDB, author_id)
    if  not author:
        raise HTTPException(status_code=404, detail= "Author not found")
    return author

@app.post("/api/user", response_model=AuthorRead)
def replace_author(author_id:int, payload: AuthorCreate, db: Session= Depends(get_db)):
    author = db.get(AuthorDB, author_id)
    if  not author:
        raise HTTPException(status_code=404, detail= "Author not found")
    
    author.name = payload.name 
    author.email = payload.email
    author.year_started = payload.year_started

    try:
        db.commit()
        db.refresh(author)
    except IntegrityError:
        db.rollback
        raise HTTPException(status_code=409, detail= "Author update failed")
    return author
    

@app.put("/api/users/{author_id}", response_model=AuthorRead)
def reaplce_author(author_id:int, payload:AuthorCreate, db: Session = Depends(get_db)):
        author = db.get(AuthorDB, author_id)
        if  not author:
            raise HTTPException(status_code=404, detail= "Author not found")
    
        author.name = payload.name 
        author.email = payload.email
        author.year_started = payload.year_started

        try:
            db.commit()
            db.refresh(author)
        except IntegrityError:
            db.rollback
            raise HTTPException(status_code=409, detail= "Author update failed")
        return author

@app.patch("/api/users/{author_id}", response_model=AuthorRead)
def reaplce_author(author_id:int, payload:AuthorCreate, db: Session = Depends(get_db)):
        author = db.get(AuthorDB, author_id)
        if  not author:
            raise HTTPException(status_code=404, detail= "Author not found")
        
        updates = payload.model_dump(exclude_unset = True)
        for fieled, value in updates.items():
            setattr(author, fieled, value)
        
        try:
            db.commit()
            db.refresh(author)
        except IntegrityError:
            db.rollback
            raise HTTPException(status_code=409, detail= "Author update failed")
        return author

    
@app.delete("/api/users/{author_id}", status_code=204)
def delete_author(author: int, db: Session = Depends(get_db)) -> Response:
    author = db.get(AuthorDB, author.id)
    if not author: 
        raise HTTPException(status_code=404, detail= "Author not found")
    db.delete(author)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT) # type: ignore


# books 
@app.get("/api/users", response_model=BooksRead)
def list_users(db: Session = Depends(get_db)):
    stmt = select(BookDB).order_by(BookDB.id)
    result= db.execute(stmt)
    Book = result.scalars().all
    return Book

@app.get("/api/users/{book_id}", response_model=BooksRead)
def get_book(book_id:int, db: Session = Depends(get_db)):
    book = db.get(BookDB, book_id)
    if  not book:
        raise HTTPException(status_code=404, detail= "Author not found")
    return book

@app.post("/api/user", response_model=BooksRead)
def replace_author(book_id:int, payload: AuthorCreate, db: Session= Depends(get_db)):
    book = db.get(AuthorDB, book_id)
    if  not book:
        raise HTTPException(status_code=404, detail= "Author not found")
    
    book.title = payload.title
    book.pages = payload.pages
    book.owner_id = payload.owner_id

    try:
        db.commit()
        db.refresh(book)
    except IntegrityError:
        db.rollback
        raise HTTPException(status_code=409, detail= "Author update failed")
    return book



    