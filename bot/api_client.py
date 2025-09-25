import requests
from typing import Dict, List, Optional

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def _headers(self, token: Optional[str] = None) -> Dict:
        headers = {'Content-Type': 'application/json'}
        if token:
            headers['Authorization'] = f'Token {token}'
        return headers

    def register_or_login(self, telegram_id: int) -> Dict:
        url = f'{self.base_url}auth/telegram/'
        data = {'telegram_id': telegram_id}
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"API error: {str(e)}")

    def get_tasks(self, token: str) -> List[Dict]:
        url = f'{self.base_url}tasks/'
        try:
            response = requests.get(url, headers=self._headers(token))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"API error: {str(e)}")

    def get_categories(self, token: str) -> List[Dict]:
        url = f'{self.base_url}categories/'
        try:
            response = requests.get(url, headers=self._headers(token))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"API error: {str(e)}")

    def create_category(self, token: str, name: str) -> Dict:
        url = f'{self.base_url}categories/'
        data = {'name': name}
        try:
            response = requests.post(url, json=data, headers=self._headers(token))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"API error: {str(e)}")

    def create_task(self, token: str, data: Dict) -> Dict:
        url = f'{self.base_url}tasks/'
        try:
            response = requests.post(url, json=data, headers=self._headers(token))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"API error: {str(e)}")