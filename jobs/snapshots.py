from fastapi import HTTPException

from core.connections import snapshots_db

async def get_all_snapshots(short_code: str, limit: int = 100, last: str = None):
    """Get all links."""
    
    response = snapshots_db.fetch(query={"short_code": short_code}, limit=limit, last=last)
    
    if response.count > 0:
        return response
    
    raise HTTPException(status_code=404, detail="No snapshots found.")