from pydantic import BaseModel


class ShortenUrlInbound(BaseModel):
    redirect_url: str

class ShortenUrlOutbound(BaseModel):
    hash: str
    redirect_url: str
