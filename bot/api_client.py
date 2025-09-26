import httpx
from typing import Dict, List, Optional

class APIClientAsync:
    def __init__(self, base_url: str, timeout: float = 10.0):
        self.base_url = base_url.rstrip("/") + "/"
        self._timeout = timeout
        self._client = httpx.AsyncClient(timeout=self._timeout)

    def _headers(self, token: Optional[str] = None) -> Dict:
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Token {token}"
        return headers

    async def register_or_login(self, telegram_id: int) -> Dict:
        url = f"{self.base_url}auth/telegram/"
        data = {"telegram_id": telegram_id}
        try:
            resp = await self._client.post(url, json=data)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as e:
            raise ValueError(f"API error: {str(e)}")

    async def get_tasks(self, token: str) -> List[Dict]:
        url = f"{self.base_url}tasks/"
        try:
            resp = await self._client.get(url, headers=self._headers(token))
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as e:
            raise ValueError(f"API error: {str(e)}")

    async def get_categories(self, token: str) -> List[Dict]:
        url = f"{self.base_url}categories/"
        try:
            resp = await self._client.get(url, headers=self._headers(token))
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as e:
            raise ValueError(f"API error: {str(e)}")

    async def create_category(self, token: str, name: str) -> Dict:
        url = f"{self.base_url}categories/"
        data = {"name": name}
        try:
            resp = await self._client.post(url, json=data, headers=self._headers(token))
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as e:
            raise ValueError(f"API error: {str(e)}")

    async def create_task(self, token: str, data: Dict) -> Dict:
        url = f"{self.base_url}tasks/"
        try:
            resp = await self._client.post(url, json=data, headers=self._headers(token))
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPError as e:
            raise ValueError(f"API error: {str(e)}")

    async def close(self):
        await self._client.aclose()