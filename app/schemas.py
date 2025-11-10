from typing import Annotated, Optional, list
from pydantic import BaseModel, EmailStr, Field, StringConstraints, ConfigDict
from annotated_types import Ge, Le 


NameStr = Annotated[str,StringConstraints(min_length=1, max_length=100)]
TitleStr = Annotated[str,StringConstraints(min_length=1, max_length=255)]
PagesStr = Annotated[str,StringConstraints(min_length=1, max_length=10000)]
YearInt = Annotated[int, Ge(1900), Le(2100)]


class AuthorCreate(BaseModel):
    name: NameStr
    email: EmailStr
    year_started: YearInt
    title: TitleStr
    pages: PagesStr

class AuthorRead(BaseModel):
    model_config= ConfigDict(from_attributes=True)
    id: int
    name: NameStr
    email: EmailStr
    year_started: YearInt

class AuthorUpdate(BaseModel):
    name: Optional[NameStr] = None 
    email: Optional[EmailStr] = None 
    year_started: Optional[YearInt] = None 
    




class BooksCreate(BaseModel):
    title: TitleStr
    pages: PagesStr

class BooksRead(BaseModel):
    model_config= ConfigDict(from_attributes=True)
    id: int
    title: TitleStr
    pages: PagesStr
    owner_id: int