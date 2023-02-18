from dataclasses import dataclass


@dataclass
class FocusToDoUrlPath:
    login: str = "v63/user/login"
    logout: str = "v60/property?client=chrome"
