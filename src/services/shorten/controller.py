from typing import Optional

from fastapi.params import Cookie
from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse

from src.configs.constants import RedisKeyCategory, RedisKeyScope, ApiRateLimit
from src.configs.env import get_settings
from src.exceptions.errors import ApiResponseResult
from src.lib.db import get_db, save_new_row, select_first
from src.lib.jwt import jwt_manager
from src.lib.redis import redis_cache
from src.schema.schema import URLModel
from src.services.shorten.serializer import ShortenUrlInbound, ShortenUrlOutbound
from src.lib.hash import hash

configs = get_settings()


class ShortenController:
    @staticmethod
    def shorten_url(request: Request,  payload: ShortenUrlInbound, token: Optional[str] = Cookie(None)):
        is_anonymous_user = True
        ip = request.client.host
        url = URLModel(
            redirect_url=payload.redirect_url,
            ip=ip
        )
        identity = ip

        print(token)

        if token:
            is_valid_token = jwt_manager.verify_token(token)
            if not is_valid_token.valid:
                return is_valid_token
            else:
                is_anonymous_user = False
                user_data = is_valid_token.payload
                identity = user_data.get('id')
                url.user_id = identity

                db = get_db()
                query = db.query(URLModel).filter(URLModel.user_id == identity and URLModel.redirect_url == payload.redirect_url)
                existing_url: Optional[URLModel] = select_first(query)

                if existing_url:
                    return JSONResponse(status_code=400, content=ApiResponseResult(success=False, data=ShortenUrlOutbound(hash=hash.encode(existing_url.id), redirect_url=existing_url.redirect_url).dict(), message="URL already has a shorten link.").to_dict())


        limit = ApiRateLimit.SHORTEN_URL_ANONYMOUS if is_anonymous_user else ApiRateLimit.SHORTEN_URL_USER

        if not redis_cache.is_allowed(identity, RedisKeyScope.SHORTEN_URL, limit, 24 * 60 * 60):
            return JSONResponse(status_code=429, content=ApiResponseResult(success=False, error="Reached limit for today!. Try again tomorrow").to_dict())
        else:
            url: URLModel  = save_new_row(url)
            short_hash = hash.encode(url.id)
            return JSONResponse(status_code=200, content=ApiResponseResult(success=True, data=ShortenUrlOutbound(hash=short_hash, redirect_url=url.redirect_url).dict()).to_dict())

    @staticmethod
    def redirect_url(request: Request, shorten_hash: str):
        db = get_db()
        url_id = hash.decode(shorten_hash)
        query = db.query(URLModel).filter(URLModel.id == url_id)
        url: Optional[URLModel] = select_first(query)

        if not url:
            return JSONResponse(status_code=404, content=ApiResponseResult(success=False, message="No such link exists").to_dict())

        return JSONResponse(status_code=200, content=ApiResponseResult(success=True, data=ShortenUrlOutbound(hash=shorten_hash, redirect_url=url.redirect_url).dict()).to_dict())
