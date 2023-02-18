from typing import Optional
from logging import getLogger

import requests
import cloudscraper


from .api_client import ApiClient
from .urls import FocusToDoUrlPath

logger = getLogger(__name__)


class FocusToDo:
    def __init__(self,
                 session_data=None,
                 additional_headers: Optional[dict] = None):
        self.session_data = session_data
        self.path = FocusToDoUrlPath()
        self.session = cloudscraper.CloudScraper()
        self.client = ApiClient(
            session=self.session,
            additional_headers=additional_headers,
        )

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
        if response.status_code != 200:
            logger.debug("Login Failed")
            return False
        logger.debug("Login Success")
        self.session_data = {
            "session_cookies": requests.utils.dict_from_cookiejar(
                self.client.get_cookies()
            ),
        }
        logger.debug("Cookies saved")
        return True

    def login(self, account: str, password: str, client: str = "Chrome") -> bool:
        # NOTE: Will be described later when
        # the process changes depending on the presence or absence of a session.
        if self.session_data is None:
            return self._auth(account, password, client)
        return self._auth(account, password, client)

    def logout(self, client: str = "chrome") -> bool:
        path: str = self.path.logout + client
        response = self.client.get(
            add_url=path,
        )
        return response.status_code == 200
