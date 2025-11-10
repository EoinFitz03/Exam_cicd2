from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint

class Base(DeclarativeBase):
    pass


class AuthorDB(Base):
    __tablename__= "Authors"
    id: Mapped[int]= mapped_column(primary_key=True)
    name: Mapped[str]= mapped_column(String(100), nullable= False)
    email: Mapped[str]= mapped_column(String(100), nullable= False)
    year_started: Mapped[int] = mapped_column(unique=True, nullable = False)

class BookDB(Base):
    __tablename__= "Books"
    id: Mapped[int]= mapped_column(primary_key=True)
    title: Mapped[str]= mapped_column(String(100), nullable= False)
    pages: Mapped[str]= mapped_column(String(100), nullable= False)
    Owner_id: Mapped[int] = mapped_column(ForeignKey("authors.id",ondelete="CASCADE", nullable= False))