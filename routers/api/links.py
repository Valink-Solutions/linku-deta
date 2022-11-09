from fastapi import APIRouter, Body, Depends, Request
from fastapi.responses import RedirectResponse

from core.auth_handler import get_current_user, get_current_user_cookie
from core.exceptions import CredentialsException

from jobs.links import create_link_code, create_short_link, delete, get_all, get_link, update_base_link
from jobs.snapshots import get_all_snapshots

from models import SnapshotResponse
from models.auth import User
from models.links import CreateLink, LinksResponse, ShowLink

from tasks.qrcodes import get_qr_code

from nanoid import generate

router = APIRouter()

@router.get("/links", response_model=LinksResponse)
async def grab_all_links(limit: int = 100, last: str = None, user: User = Depends(get_current_user)):
    return await get_all(limit, last)

@router.post("/links", response_model=ShowLink)
async def shorten_link(link_data: CreateLink = Body(...), user: User = Depends(get_current_user)):
    return await create_short_link(link_data)

@router.post("/cookie/links", response_model=ShowLink)
async def shorten_link(request: Request):
    
    try:
        await get_current_user_cookie(request.cookies.get("access_token"))
    except CredentialsException:
    
        response = RedirectResponse(url="/login", status_code=302)
        response.delete_cookie(key="access_token")
        
        return response
    
    data = await request.form()
    
    short_code = data.get("short_code") or generate(size=6)
        
    link_data = CreateLink(title=data["title"], short_code=short_code, long_url=data["long_url"])
    
    await create_short_link(link_data)
    
    return RedirectResponse(url="/dashboard/home", status_code=302)

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