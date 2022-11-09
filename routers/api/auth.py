from fastapi import APIRouter, Response, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

from core.auth_handler import get_current_user

from jobs.auth import authenticate_user, user_logout
from models.auth import User


router = APIRouter()


@router.post("/cookie/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    data = await authenticate_user(form_data)
    
    response = RedirectResponse(url="/dashboard/home", status_code=302)
    
    response.set_cookie(key="access_token", value=f"Bearer {data.access_token}", httponly=True)
    
    return response


@router.post("/jwt/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    
    return await authenticate_user(form_data)


@router.post("/jwt/logout")
async def logout(user: User = Depends(get_current_user)):
    return await user_logout(user)
