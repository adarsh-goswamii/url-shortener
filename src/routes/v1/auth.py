from fastapi import APIRouter, Request
from src.services.auth.controller import AuthController

router = APIRouter()

@router.get("/token")
async def get_token(request: Request, auth_code: str):
    return await AuthController.get_token(request, auth_code)