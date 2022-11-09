from typing import Optional
from fastapi import APIRouter, Request, Depends, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core.auth_handler import get_current_user_cookie
from jobs.dashboard import get_dashboard

from models.auth import User

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/dashboard/home", response_class=HTMLResponse)
async def read_dashboard(request: Request, limit: int = 1, last: Optional[str] = None):
    return await get_dashboard(last, limit, request=request)

@router.get("/dashboard/new_link", response_class=HTMLResponse)
async def read_new_link(request: Request):
    return templates.TemplateResponse("new_link.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})