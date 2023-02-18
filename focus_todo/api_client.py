from logging import getLogger
from typing import Optional, Tuple

from .exceptions import (
    FocusToDoConnectionError,
    FocusToDoTooManyRequestsError,
    FocusToDoAuthenticationError
)

logger = getLogger(__name__)


class ApiClient:
    BASE_URL: str = "oversea.focustodo.net"
    ua: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    default_headers: dict = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "sec-ch-ua-platform": "Windows",
        "user-agent": ua,
    }

    def __init__(self, session, headers: Optional[dict] = None, additional_headers: Optional[dict] = None):
        self.session = session
        self.headers = self.default_headers.copy()
        if type(headers) is dict:
            self.headers = headers
        if type(additional_headers) is dict:
            self.headers.update(additional_headers)

    def set_cookies(self, cookies):
        logger.debug("Restoring cookies for saved session")
        self.session.cookies.update(cookies)

    def get_cookies(self):
        return self.session.cookies

    def clear_cookies(self):
        self.session.cookies.clear()

    def url(self, add_url: Optional[str] = None) -> str:
        path: str = f"https:{self.BASE_URL}"
        if type(add_url) is str:
            path += f"/{add_url}"
        return path

    def _get_headers(self, additional_headers: Optional[dict] = None) -> dict:
        headers = self.headers.copy()
        if type(additional_headers) is dict:
            headers.update(additional_headers)
        return headers

    def _get_req_info(self, additional_headers: Optional[dict], add_url: Optional[str]) -> Tuple[dict, str]:
        headers = self._get_headers(additional_headers=additional_headers)
        url: str = self.url(add_url)
        return headers, url

    def get(self, add_url: Optional[str] = None, additional_headers: Optional[dict] = None, params: Optional[dict] = None):
        headers, url = self._get_req_info(additional_headers, add_url)
        logger.debug(f"URL: {url}")
        logger.debug(f"Headers: {headers}")
        try:
            response = self.session.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response
        except Exception as err:
            logger.debug(f"Response in exception: {err}")
            if response.status_code == 429:
                raise FocusToDoTooManyRequestsError(
                    "Too many requests"
                ) from err
            if response.status_code == 401:
                raise FocusToDoAuthenticationError(
                    "Authentication error"
                ) from err
            if response.status_code == 403:
                raise FocusToDoConnectionError(
                    f"Forbidden url: {url}"
                ) from err
            raise FocusToDoConnectionError(err) from err

    def post(self, add_url: Optional[str] = None, additional_headers: Optional[dict] = None,
             params: Optional[dict] = None, data: Optional[str] = None, files: Optional[str] = None):
        headers, url = self._get_req_info(additional_headers, add_url)
        logger.debug(f"URL: {url}")
        logger.debug(f"Headers: {headers}")
        logger.debug(f"Data: {data}")
        try:
            response = self.session.post(
                url, data=data, headers=headers, params=params, files=files)
            response.raise_for_status()
            return response
        except Exception as err:
            logger.debug(f"Response in exception: {err}")
            if response.status_code == 429:
                raise FocusToDoTooManyRequestsError(
                    "Too many requests"
                ) from err
            if response.status_code == 401:
                raise FocusToDoAuthenticationError(
                    "Authentication error"
                ) from err
            if response.status_code == 403:
                raise FocusToDoConnectionError(
                    f"Forbidden url: {url}"
                ) from err
            raise FocusToDoConnectionError(err) from err
