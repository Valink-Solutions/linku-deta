from fastapi import APIRouter, BackgroundTasks, Depends
from core.auth_handler import get_current_user
from models.auth import User

from routers.api import links, auth, user
from tasks.snapshots import csd_non_cron

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(user.router, prefix="/users", tags=["users"])
router.include_router(links.router, tags=["links"])


@router.post("/force_snapshots", tags=["snapshots"])
async def force_snapshots(background_tasks: BackgroundTasks, user: User = Depends(get_current_user)):
    """Force snapshots to be taken."""
    
    background_tasks.add_task(csd_non_cron)
    
    return {"message": "Snapshots will be taken shortly."}
    