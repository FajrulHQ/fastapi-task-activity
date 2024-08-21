from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import APIRouter, Request
from . import schemas, crud
from app.config import database, settings
from datetime import timedelta

router = APIRouter()
module = 'auth'
route = f"/{module}"

@router.post("/users/", tags=[module], response_model=schemas.User)
def create_user(
    user: schemas.UserCreate, 
    db: Session = Depends(database.get_db)
):
    # Check if the username or email is already taken
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    return crud.create_user(db=db, user=user)

@router.get("/users/me/", tags=[module], response_model=schemas.User)
async def read_users_me(
    user: schemas.User = Depends(crud.verify_token)
):
    return user

@router.post("/login/", tags=[module], response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(database.get_db)
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}