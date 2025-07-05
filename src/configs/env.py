import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    env: str            = os.getenv("ENV", "local")
    db_user: str        = os.getenv("DB_USER", "user")
    db_password: str    = os.getenv("DB_PASSWORD", "user")
    db_host: str        = os.getenv("DB_HOST", "0.0.0.0")
    db_name: str        = os.getenv("DB_NAME", "central_db")

    redis_port: int = os.getenv("REDIS_PORT", 6379)
    redis_host: str = os.getenv("REDIS_HOST", "0.0.0.0")

    jwt_public_key: str = os.getenv("JWT_PUBLIC_KEY", "sample")

    auth_service_domain: str = os.getenv("AUTH_SERVICE_DOMAIN", "http://localhost:8001")

    application_id: str = os.getenv("APPLICATION_ID", "url_shortener")

    hash_secret_key: int = os.getenv("HASH_SECRET", 982374928374)

@lru_cache
def get_settings():
    return BaseConfig()