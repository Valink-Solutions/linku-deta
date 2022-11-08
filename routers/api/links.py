from fastapi import APIRouter, Body, Depends

from core.auth_handler import get_current_user

from jobs.links import create_link_code, create_short_link, delete, get_all, get_link, update_base_link
from jobs.snapshots import get_all_snapshots

from models import SnapshotResponse
from models.auth import User
from models.links import CreateLink, LinksResponse, ShowLink

from tasks.qrcodes import get_qr_code

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

@router.get("/links/{short_code}/snapshots", response_model=SnapshotResponse)
async def get_snapshots(short_code: str, user: User = Depends(get_current_user)):
    return await get_all_snapshots(short_code)

@router.post("/settings")
async def update_settings(link: str, user: User = Depends(get_current_user)):
    return update_base_link(link)