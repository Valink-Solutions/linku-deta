from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from core.auth_handler import get_current_user_cookie
from core.connections import url_db, settings_db
from core.exceptions import CredentialsException

templates = Jinja2Templates(directory="templates")

async def get_dashboard(last: str = None, limit: int = 100, *, request: Request) -> templates.TemplateResponse:
    
    try:
        await get_current_user_cookie(request.cookies.get("access_token"))
    except CredentialsException:
    
        response = RedirectResponse(url="/login", status_code=302)
        response.delete_cookie(key="access_token")
        
        return response
    
    link_results = url_db.fetch(query=None, last=last, limit=limit)
    settings_results = settings_db.get("APP_URL")
    
    links = link_results.items
    
    return templates.TemplateResponse("dashboard.html", {"request": request, "links": links, "count": link_results.count, "app_url": settings_results["APP_URL"], "last_key": last, "new_last": link_results.last})