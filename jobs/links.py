from nanoid import generate

from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder

from core import settings
from core.connections import url_db
from models.links import CreateLink, LinkInDB
from tasks.qrcodes import create_qr_code, get_qr_code, upload_qr_code


async def create_short_link(link_data: CreateLink):
    """Shorten a link."""
    
    if link_data.short_code:
        short_code = link_data.short_code
    else:
        short_code = generate(size=8)
        
    link = jsonable_encoder(LinkInDB(
        title=link_data.title,
        long_url=link_data.long_url,
        # is_protected=link_data.is_protected,
    ))
    
    existing_link = url_db.get(short_code)
    
    if existing_link:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail="Short code already in use.")
    
    try:
        url_db.insert(link, short_code)
        
        new_link = url_db.get(short_code)
        
        return new_link
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Could not create link.")
    
async def get_link(short_code: str):
    """Get a link."""
    
    link = url_db.get(short_code)
    
    if link:
        return link
    else:
        raise HTTPException(status_code=404, detail="Link not found.")
    
async def get_all(limit: int = 100, last: str = None):
    """Get all links."""
    
    response = url_db.fetch(query=None, limit=limit, last=last)
    
    if response.count > 0:
        return response
    
    raise HTTPException(status_code=404, detail="No links found.")
    
async def redirect_to_link(short_code: str, request: Request):
    """Get a link."""
    
    link = url_db.get(short_code)
    
    if link:
        
        url_db.update({"daily_clicks": link["daily_clicks"] + 1}, short_code)
        
        return RedirectResponse(url=link["long_url"])
    else:
        raise HTTPException(status_code=404, detail="Link not found.")
    
    
async def delete(short_code: str):
    """Delete a link."""
    
    link = url_db.get(short_code)
    
    if link:
        url_db.delete(short_code)
        return {"message": "Link deleted."}
    else:
        raise HTTPException(status_code=404, detail="Link not found.")
    

async def create_link_code(short_code: str):
    """Create a link code."""
    
    link = url_db.get(short_code)
    
    if link:
        create_qr_code(short_code)
        upload_qr_code(short_code)
        return get_qr_code(short_code)
    else:
        raise HTTPException(status_code=404, detail="Link not found.")