from typing import Optional
from logging import getLogger

import requests
import cloudscraper


from .api_client import ApiClient
from .urls import FocusToDoUrlPath

logger = getLogger(__name__)


class FocusToDo:
    def __init__(self, session_data=None, additional_headers: Optional[dict] = None):
        self.session_data = session_data
        self.path = FocusToDoUrlPath()
        self.session = cloudscraper.CloudScraper()
        self.client = ApiClient(
            session=self.session,
            additional_headers=additional_headers,
        )

    def _login_session(self):
        logger.debug("Login with cookies")
        logger.debug("Set cookies in session")
        self.client.set_cookies(
            requests.utils.cookiejar_from_dict(
                self.session_data["session_cookies"])
        )
        self.client.set_cookies(
            requests.utils.cookiejar_from_dict(
                self.session_data["login_cookies"])
        )
        logger.debug("Get page data with cookies")

    def _auth(self, account: str, password: str, client: str):
        logger.debug(f"login: {account}")
        logger.debug(f"login: {client}")
        self.client.clear_cookies()
        params: dict = {
            "account": account,
            "password": password,
            "client": client,
        }
        response = self.client.post(
            add_url=self.path.login,
            params=params,
        )
        # TODO:Describe the process of saving sessions
        print(response.status_code)
        print(response.json())

    def login(self, account: str, password: str, client: str = "Chrome"):
        if self.session_data is None:
            return self._auth(account, password, client)
        return self._login_session()
