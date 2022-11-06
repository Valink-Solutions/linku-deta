from fastapi import APIRouter

from routers.api import links

router = APIRouter()

router.include_router(links.router, tags=["links"])