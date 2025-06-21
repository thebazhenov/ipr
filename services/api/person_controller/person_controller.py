from services import BaseApiClient
from requests import Response


class PersonController(BaseApiClient):
    def get_users(self) -> Response:
        return self._request("GET", "/users")

    def post_user(self, data: dict) -> Response:
        return self._request("POST", "/user", json=data)

    def get_user(self, user_id: int) -> Response:
        return self._request("GET", f"/user/{user_id}")