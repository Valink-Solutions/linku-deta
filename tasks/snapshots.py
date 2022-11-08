from deta import app

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from core.connections import snapshots_db, url_db
from models import Snapshot

def create_snapshot(snapshot_data: Snapshot):
    """Create a snapshot."""
    
    try:
        new_snapshot = snapshots_db.insert(jsonable_encoder(snapshot_data))
        
        return new_snapshot
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Could not create snapshot.")
    
@app.lib.cron()
def create_snapshot_data(event):
    """Creates all snapshots for all links."""
    
    response = url_db.fetch(query=None, limit=1000, last=None)
    
    if response.count > 0:
    
        for item in response.items:
            create_snapshot(Snapshot(short_code=item["key"], clicks=item["daily_clicks"]))
            url_db.update({"daily_clicks": 0}, item["key"])
            
def csd_non_cron():
    """Creates all snapshots for all links."""
    
    response = url_db.fetch(query=None, limit=1000, last=None)
    
    if response.count > 0:
    
        for item in response.items:
            create_snapshot(Snapshot(short_code=item["key"], clicks=item["daily_clicks"]))
            url_db.update({"daily_clicks": 0}, item["key"])
            
