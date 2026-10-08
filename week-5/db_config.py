from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv()
db_url=os.getenv("DATABASE_URL")

engine = create_engine(db_url, connect_args={"check_same_thread": False}, echo=True)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass


Base.metadata.create_all(engine)
