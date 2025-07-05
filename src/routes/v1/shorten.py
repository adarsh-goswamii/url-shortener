from typing import Optional

from fastapi import APIRouter, Request
from fastapi.params import Cookie

from src.services.shorten.controller import ShortenController
from src.services.shorten.serializer import ShortenUrlInbound

router = APIRouter()


@router.post("")
async def shorten_url(request: Request, payload: ShortenUrlInbound, token: Optional[str] = Cookie(None)):
    return ShortenController.shorten_url(request, payload, token)

@router.get("")
async def get_redirect_url(request: Request, shorten_hash: str):
    return ShortenController.redirect_url(request, shorten_hash)