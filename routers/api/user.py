
from fastapi import APIRouter, Depends

from core.auth_handler import get_current_user

from models.auth import User

router = APIRouter()

@router.get("/me", response_model=User)
async def current_user(user: User = Depends(get_current_user)):
    return user