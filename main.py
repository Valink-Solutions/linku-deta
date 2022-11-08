from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from jobs.links import redirect_to_link

from routers import api, pages

from core import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="""
# Linku by Valink Solutions

This is a url shortener app built with FastAPI. Linku allows you to shorten links, create dynamic qr codes, and share link trees.
""",
    version=settings.APP_VERSION
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(pages.router)
app.include_router(api.router, prefix="/api")

@app.get("/{short_code}")
async def get_link(short_code: str, request: Request):
    return await redirect_to_link(short_code, request)