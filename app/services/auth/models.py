from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.config.database import Base

class User(Base):
    __tablename__   = "users"

    id              = Column(Integer, primary_key=True, index=True)
    username        = Column(String, unique=True, index=True)
    fullname        = Column(String)
    hashed_password = Column(String)
    created_at      = Column(DateTime, default=datetime.now)
    updated_at      = Column(DateTime, default=datetime.now)