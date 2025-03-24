import httpx
from urllib.parse import urljoin
from helpers.clients.http_client import BaseApiClient

from src.errors.service import UserServiceIsUnavailableError
from src.settings import get_settings


class UsersClient(BaseApiClient):
    _base_url = str(get_settings().base_users_url)

    async def get_user_info(self, user_id: str) -> httpx.Response:
        try:
            response = await self.get(url=urljoin(self._base_url, '/users/'), params={'user__id': [user_id]})
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise UserServiceIsUnavailableError from e
        return response
