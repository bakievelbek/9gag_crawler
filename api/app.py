import logging

from fastapi import FastAPI
from fastapi import APIRouter

from .routes import crawl

app = FastAPI()

api_router = APIRouter()

api_router.include_router(crawl.router, prefix="", tags=["crawl"])

app.include_router(api_router)

logging.info("APP INITIALIZED")
