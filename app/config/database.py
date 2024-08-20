import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from . import settings

load_dotenv()

DATABASE_URL = f"postgresql://{settings.MAIN_DB_USER}:{settings.MAIN_DB_PASSWORD}@"\
               f"{settings.MAIN_DB_HOST}:{settings.MAIN_DB_PORT}/{settings.MAIN_DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
