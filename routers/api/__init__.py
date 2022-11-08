from fastapi import APIRouter

from routers.api import links, auth, user

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(user.router, prefix="/users", tags=["users"])
router.include_router(links.router, tags=["links"])