from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import api, pages

from core import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="""
# Url Shortener 

This is a url shortener app built with FastAPI. Linku allows you to shorten links, create dynamic qr codes, and share link trees.
""",
    version=settings.APP_VERSION
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(pages.router)
app.include_router(api.router, prefix="/api")