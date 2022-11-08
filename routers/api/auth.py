from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from core.auth_handler import get_current_user

from jobs.auth import authenticate_user, user_logout
from models.auth import User


router = APIRouter()


@router.post("/jwt/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await authenticate_user(form_data)


@router.post("/jwt/logout")
async def logout(user: User = Depends(get_current_user)):
    return await user_logout(user)
