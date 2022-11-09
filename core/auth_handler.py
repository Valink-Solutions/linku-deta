from datetime import datetime, timedelta
from time import time
from typing import Optional

from fastapi import HTTPException, status, Depends, Cookie
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from core import settings
from core.connections import auth_db
from core.exceptions import CredentialsException

from models import Token, TokenData
from models.auth import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/jwt/login")


def create_access_token(user_email: str, expires_delta: Optional[timedelta] = None) -> Token:
    
    to_encode = TokenData(email=user_email).dict()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.APP_SECRET, algorithm=settings.APP_ALGORITHM)
    
    return Token(access_token=encoded_jwt)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.APP_SECRET, algorithms=[settings.APP_ALGORITHM])
        
        email: str = payload.get("email")
        exp: time = payload.get("exp")
    
        if email is None:
            raise credentials_exception
        
        if float(exp) <= time():
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    if not email == settings.ADMIN_EMAIL:
        raise credentials_exception
    
    return User(email=email)


async def get_current_user_cookie(token: str) -> User:
    
    credentials_exception = CredentialsException("Could not validate credentials")
    
    try:
        if not token:
            raise credentials_exception
        
        if token.startswith("Bearer "):
            token = token[7:]
        
        payload = jwt.decode(token, settings.APP_SECRET, algorithms=[settings.APP_ALGORITHM])
        
        email: str = payload.get("email")
        exp: time = payload.get("exp")
    
        if email is None:
            raise credentials_exception
        
        if float(exp) <= time():
            raise credentials_exception
        
        if email != settings.ADMIN_EMAIL:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    return User(email=email)