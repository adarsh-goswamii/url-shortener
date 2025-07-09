import httpx
from fastapi import Request, HTTPException
import base64

from starlette.responses import JSONResponse

from src.configs.env import get_settings
from src.lib.http_client import http_client


class AuthController:
    @staticmethod
    async def get_token(request: Request, auth_code: str):
        configs = get_settings()
        application_id, application_secret = configs.application_id, configs.application_secret
        encoded_app_data = base64.b64encode(f'{application_id}:{application_secret}'.encode()).decode()

        try:
            response = await http_client.get(url=f'{configs.auth_service_domain}?auth_code={auth_code}', headers={
                "Authorization": f"Basic {encoded_app_data}"
            })

        except httpx.HTTPStatusError as error:
            raise HTTPException(status_code=error.response.status_code, detail=error.response.json().get("detail", "Something went wrong!"))

        return_data = JSONResponse(status_code=200, content=response.json())
        return_data.set_cookie(key="token", value=response.json().get("token"), httponly=True, max_age=60 * 60 * 4, secure=True, samesite="lax")

        return return_data
