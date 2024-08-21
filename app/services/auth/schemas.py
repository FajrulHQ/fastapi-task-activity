from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username        : str
    fullname        : str

class UserCreate(User):
    password        : str
    
# JWT Token schemas
class Token(BaseModel):
    access_token    : str
    token_type      : str

class TokenData(BaseModel):
    username        : Optional[str]     = None