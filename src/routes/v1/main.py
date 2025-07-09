from fastapi import APIRouter
from src.routes.v1 import shorten, auth

api_router = APIRouter()

api_router.include_router(shorten.router, prefix='/v1/shorten', tags=["Shorten URL"])
api_router.include_router(auth.router, prefix='/v1/auth', tags=["Auth"])