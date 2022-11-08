import logging
from time import time

from fastapi import HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from passlib.context import CryptContext

from core import settings
from core.connections import auth_db
from core.auth_handler import create_access_token

from models.auth import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(data: OAuth2PasswordRequestForm):
    
    
    if not data.username == settings.ADMIN_EMAIL:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username: {data.username} not found.")
    
    if not data.password == settings.ADMIN_PASSWORD:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Incorrect password.")    
    
    return create_access_token(settings.ADMIN_EMAIL)
    
    
async def user_logout(user: User):
    # user.is_active = False
    
    # session.add(user)
    # await session.commit()
    # await session.refresh(user)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "User successfully logged out."})