from fastapi import APIRouter, Body, Depends
from jobs.links import create_link_code, create_short_link, delete, get_all, get_link

from models.links import CreateLink, LinksResponse, ShowLink
from tasks.qrcodes import get_qr_code

from core.auth_handler import get_current_user

from models.auth import User

router = APIRouter()

@router.get("/links", response_model=LinksResponse)
async def grab_all_links(limit: int = 100, last: str = None, user: User = Depends(get_current_user)):
    return await get_all(limit, last)

@router.post("/links", response_model=ShowLink)
async def shorten_link(link_data: CreateLink = Body(...), user: User = Depends(get_current_user)):
    return await create_short_link(link_data)

@router.get("/links/{short_code}", response_model=ShowLink)
async def grab_link(short_code: str, user: User = Depends(get_current_user)):
    return await get_link(short_code)

@router.delete("/links/{short_code}")
async def delete_link(short_code: str, user: User = Depends(get_current_user)):
    return await delete(short_code)

@router.post("/links/{short_code}/code")
async def create_code(short_code: str, user: User = Depends(get_current_user)):
    return await create_link_code(short_code)

@router.get("/links/{short_code}/code")
async def get_code(short_code: str, user: User = Depends(get_current_user)):
    return get_qr_code(short_code)