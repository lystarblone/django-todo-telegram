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
        return {'token': 'test-token', 'user_id': telegram_id}

    def get_tasks(self, token: str) -> List[Dict]:
        return [
            {'id': 1, 'title': 'Test Task', 'category': {'name': 'Work'}, 'created_at': '2025-09-25T15:00:00Z'}
        ]

    def get_categories(self, token: str) -> List[Dict]:
        return [{'id': 1, 'name': 'Work'}, {'id': 2, 'name': 'Personal'}]

    def create_category(self, token: str, name: str) -> Dict:
        return {'id': 3, 'name': name}

    def create_task(self, token: str, data: Dict) -> Dict:
        return {'id': 2, 'title': data['title'], 'category': {'name': 'Work'}}