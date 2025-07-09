import httpx
from typing import Optional, Dict, Any


class HTTPClient:
    def __init__(self, default_headers: Optional[Dict[str, str]] = None):
        self.default_headers = default_headers or {}

    async def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        async with httpx.AsyncClient(headers={**self.default_headers, **(headers or {})}) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response

    async def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        async with httpx.AsyncClient(headers={**self.default_headers, **(headers or {})}) as client:
            response = await client.post(url, data=data, json=json)
            response.raise_for_status()
            return response

    async def put(
        self,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        async with httpx.AsyncClient(headers={**self.default_headers, **(headers or {})}) as client:
            response = await client.put(url, json=json)
            response.raise_for_status()
            return response

    async def delete(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
    ):
        async with httpx.AsyncClient(headers={**self.default_headers, **(headers or {})}) as client:
            response = await client.delete(url)
            response.raise_for_status()
            return response

http_client = HTTPClient()