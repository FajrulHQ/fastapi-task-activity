from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username      : str
    fullname      : str

class UserCreate(UserBase):
    password      : str

class UserLogin(BaseModel):
    username: str
    password: str
    
# JWT Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None